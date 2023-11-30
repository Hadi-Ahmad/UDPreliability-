import socket
import json
import os
import urllib.parse
import re

def getHTTP(host, port, givenResource, params, headers, verbose):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        # print("Type any thing then ENTER. Press Ctrl+C to terminate")
        resource = givenResource
        headers_str = "" # Construct the HTTP request headers dynamically
        if params:
            query = "&".join([f"{key}={value}" for key, value in params.items()])
            resource = f"{givenResource}?{query}"
        if (headers):
            for key, value in headers.items():
                headers_str += f"{key}: {value}\r\n"
                # print(headers_str)
            line = f"GET {resource} HTTP/1.0\r\nHost: {host}\r\n{headers_str}\r\n"
        else:
            line = f"GET {resource} HTTP/1.0\r\nHost: {host}\r\n\r\n"

        request = line.encode("utf-8")
        conn.sendall(request)
        response = b''
        # MSG_WAITALL waits for full request or error
        # response = conn.recv(len(request), socket.MSG_WAITALL)
        while True:
            chunk = conn.recv(4096)  # Receive up to 1024 bytes at a time
            if not chunk:
                break  # No more data to receive, exit the loop
            response += chunk   
        response = response.decode("utf-8")
        res = response
        header, body = response.split('\n\r')

        # Split the response into lines
        response_lines = header.splitlines()
        # Extract the status line (first line)
        status_line = response_lines[0]
        # Split the status line into its components
        http_version, status_code, status_message = status_line.split(' ', 2)

    finally:
        conn.close()
        if(verbose):
            print("\nResponse: \n" + res + "\n")
        else:
            print("\nResponse: \n" + body + "\n")
        if(status_code =="301" or status_code =="302"):
            print("Redirect... \n")
            newHost = getlocation(header)
            print("New url:", host+newHost)
            getHTTP(host, port, newHost, params, headers, verbose)

def postHTTP(host, port, givenResource, params, filepath, headers, verbose):

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, 80))
        # print("Type any thing then ENTER. Press Ctrl+C to terminate")
        resource = givenResource  # The resource you want to request
        headers_str = "" # Construct the HTTP request headers dynamically
        data = params
        contentType = ""

        if isinstance(data, str):
            data = data.encode("utf-8")
            length_in_bytes = len(data)
            data = data.decode("utf-8")
            contentType = "text/html"

        elif isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
            encoded_str = data.encode('utf-8')
            length_in_bytes = len(encoded_str)
            contentType = "application/json"

        elif (filepath):
            # print(filepath)
            # Get the file name from the file path
            file = open(filepath, "r")
            data = file.read()
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            length_in_bytes = filesize
            contentType = "multipart/form-data"

        if (headers):
            for key, value in headers.items():
                headers_str += f"{key}: {value}\r\n"
            line = f"POST {resource} HTTP/1.0\r\nHost: {host}\r\n{headers_str}Content-Length: {length_in_bytes}\r\n\r\n"
        
        if contentType == "multipart/form-data":
            print("sending File..\n")

            # # Construct the multipart/form-data body
            boundary = '----Boundary1234567890'
            
            body = []
            body.append(f'--{boundary}')
            body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"')
            body.append('Content-Type: application/octet-stream')
            body.append('')  # Add an empty line to separate headers from the file content
            body.append(data)  # Add the file content
            body.append(f'--{boundary}--')
            

            # # Join the body parts and send them
            body_data = '\r\n'.join(body)

            # # Update the Content-Length header
            length_in_bytes = len(body_data.encode())
            
            # Update the request line to include the Content-Length and Content-Type headers
            line = f"POST {resource} HTTP/1.0\r\nHost: {host}\r\n{headers_str}Content-Length: {length_in_bytes}\r\nContent-Type: multipart/form-data; boundary={boundary}\r\n\r\n"

            # Send the request line and the multipart/form-data body
            conn.sendall((line + body_data).encode())

        else:
            print("sedning text/json..")
            print(length_in_bytes)
            # For JSON or string payloads, send the data in the request body
            line = f"POST {resource} HTTP/1.0\r\nHost: {host}\r\n{headers_str}Content-Length: {length_in_bytes}\r\n\r\n{data}"
            # line += f"{data}"
            request = line.encode("utf-8")
            conn.sendall(request)

        response = response = b''
        n = 0
        # # MSG_WAITALL waits for full request or error
        while n<10:
            chunk = conn.recv(1024)  # Receive up to 1024 bytes at a time
            n +=1
            if not chunk:
                break  # No more data to receive, exit the loop
            response += chunk
        response = response.decode("utf-8")
        res = response
        header, body = response.split('\n\r')

        # Split the response into lines
        response_lines = header.splitlines()
        # Extract the status line (first line)
        status_line = response_lines[0]
        # Split the status line into its components
        http_version, status_code, status_message = status_line.split(' ', 2)

    finally:
        conn.close()
        if(verbose):
            print("\nResponse: \n" + res + "\n")
        else:
            print("\nResponse: \n" + body + "\n")
        if(status_code =="301" or status_code =="302"):
            print("Redirect... \n")
            newHost = getlocation(header)
            print("New url:", host+newHost)
            postHTTP(host, port, newHost, params, filepath, headers, verbose)

def getlocation(res):
    pattern = r'location:\s*(\S+)'
    # Use re.search to find the match in the input string
    match = re.search(pattern, res, re.IGNORECASE)
    location_value = match.group(1)
    return location_value

def get_port_from_url(url):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.port:
        return parsed_url.port
    elif parsed_url.scheme == "http":
        return 80  # Default HTTP port
    elif parsed_url.scheme == "https":
        return 443  # Default HTTPS port
    else:
        return None  # Port not specified or recognized scheme