import socket
import os
import json
import re
import threading
import time

def serverRun(path,recRequest):
    """
    Start a simple HTTP server that listens for incoming connections and serves files
    from the 'data' directory. The server responds to the 'GET /' request with a list
    of files in the 'data' directory, formatted based on the 'Accept' header of the request.
    """

        # Get the client request
    request = recRequest

    # Parse HTTP headers from the request
    headers = request.split('\n')

    # Check the HTTP method
    method = headers[0].split()[0]

    filename = headers[0].split()[1]
    # print(filename)
        
    if method.upper() == 'GET':
        # Extract the 'Accept' header to determine the desired response format
        accept_header = [header.split(":")[1].strip() for header in headers if header.startswith("Accept:")]
        accept_format = accept_header[0] if accept_header else "application/json"  # Default to JSON
            
        # Handle different routes
        full_path = f'{path}{filename}'

        # Normalize the path and check for directory traversal
        normalized_path = os.path.normpath(full_path)
        base_directory = os.path.normpath(path)

        if not normalized_path.startswith(base_directory):
            # print(full_path)
            # print("normalized path:",normalized_path)
            # print("base path",base_directory)
            response = 'HTTP/1.0 403 FORBIDDEN\r\n\r\nDirectory traversal attempt detected!'
            

            
        # Check if the path corresponds to a directory within 'data'
        if os.path.isdir(full_path):
            files = os.listdir(full_path)
                
            # Format the response based on the 'Accept' header
            if "application/json" in accept_format:
                response = 'HTTP/1.0 200 OK\r\n\r\n' + json.dumps(files)
            elif "text/plain" in accept_format:
                response = 'HTTP/1.0 200 OK\r\n\r\n' + '\n'.join(files)
            elif "text/html" in accept_format:
                files_html = ''.join([f"<li>{file}</li>" for file in files])
                response = f'HTTP/1.0 200 OK\r\n\r\n<ul>{files_html}</ul>'
            else:
                response = 'HTTP/1.0 200 OK\r\n\r\n' + json.dumps(files)  # Default to JSON
            
        # Check if the path corresponds to a file within 'data'
        else:
            # Get the directory and base name from the full path
            directory, base_name = os.path.split(full_path)
            # print(directory)
                
            # Look for files in the directory that start with the base name
            matching_files = [f for f in os.listdir(directory) if f.startswith(base_name)]
                
            if matching_files:
                actual_file = os.path.join(directory, matching_files[0])
                try:
                    with open(actual_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    response = 'HTTP/1.0 200 OK\r\n\r\n' + content
                except Exception as e:
                    print(f"Error reading file: {e}")
                    response = 'HTTP/1.0 500 INTERNAL SERVER ERROR\r\n\r\nInternal Server Error!'
            else:
                response = 'HTTP/1.0 404 NOT FOUND\r\n\r\nFile not found!'

    elif method.upper() == 'POST':
        lock = threading.Lock()
        lock.acquire()
        time.sleep(2)
        # Extract the body content from the request
        body = request.split('\r\n\r\n')[1]
        # print("Body is:",body)
            
        # Determine the path where the file should be created or overwritten
        file_path = os.path.join(path, filename.lstrip('/'))
            
        # Check for directory traversal
        normalized_path = os.path.normpath(file_path)
        base_directory = os.path.normpath(path)
        if not normalized_path.startswith(base_directory):
            response = 'HTTP/1.0 403 FORBIDDEN\r\n\r\nDirectory traversal attempt detected!'
            
            
        # Write the content to the file
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(body)
            response = 'HTTP/1.0 200 OK\r\n\r\nFile created/overwritten successfully!'
        except Exception as e:
            print(f"Error writing to file: {e}")
            response = 'HTTP/1.0 500 INTERNAL SERVER ERROR\r\n\r\nInternal Server Error!'
        finally:
            lock.release()

    else:
        response = 'HTTP/1.0 405 METHOD NOT ALLOWED\n\nMethod not allowed!'
        
    return response