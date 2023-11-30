#this function is used to check content type wether its file, json or string 

# def checkcontenttype(contentType):
    # contenttype = contentType
    # if(contenttype == "application/json"):

    # elif (contenttype == "multipart/form-data"):
    #         # File upload
    #         file_path = params.get("file_path", "")
    #         with open(file_path, "rb") as file:
    #             file_data = file.read()
    #             length_in_bytes = len(file_data)
    #         contentType = "multipart/form-data"
    # return contentType

#application/x-www-form-urlencoded for URL-encoded form data

# In an HTTP request, the "body" refers to the part of the request message that contains the data being sent from the client (the requester) to the server. The body is typically used to transmit data such as form submissions, JSON payloads, file uploads, or any other data that needs to be sent to the server for processing. The format and content of the body depend on the HTTP method and the specific requirements of the server and application.

# Here are a few key points about the body of an HTTP request:

# HTTP Methods: Different HTTP methods use the request body differently:
# GET: Generally does not have a request body. Any data is typically sent in the query parameters of the URL.
# POST: Commonly used to send data in the request body, such as form data or JSON payloads.
# PUT: Used to update an existing resource. The request body often contains the updated data.
# DELETE: Typically does not have a request body, as it's used to delete a resource identified by the URL.
# Content-Type Header: The Content-Type header in the HTTP request specifies the media type of the data in the request body. It helps the server understand how to interpret the data in the body. Common Content-Type values include:
# application/json for JSON data
# application/x-www-form-urlencoded for URL-encoded form data
# multipart/form-data for file uploads and more complex form data
# Request Body Format: The format of the request body depends on the Content-Type. For example:
# In a JSON request body, data is typically serialized as a JSON object.
# In a URL-encoded form, data is sent as key-value pairs.
# In a multipart/form-data request, data can include files and form fields.
# Binary Data: HTTP request bodies can contain binary data, such as files, images, or any binary payload. In this case, the body may be treated as binary and may not be directly human-readable.
# Size Limitations: The size of the request body may be limited by server or network constraints. Large payloads may need to be split into smaller parts or handled in a streaming fashion.
# Security: Security considerations are crucial when handling request bodies, especially when accepting data from untrusted sources. Input validation, sanitization, and proper handling of sensitive data are important.
# Here's an example of a POST request with a JSON request body:




# #Creating boundary
# name = "file"
# boundary_ = "boundary_value"
# multipart_body = f'--boundary_value\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n[base64-encoded file content]\r\n--boundary_value--\r\n'

# # Update the request line to include the Content-Length and Content-Type headers
# line = f"POST {resource} HTTP/1.0\r\nHost: {host}\r\nContent-Type: multipart/form-data; boundary={boundary_}\r\nContent-Length: {length_in_bytes}\r\n\r\n"

# # Send the HTTP request line and headers
# conn.sendall(line.encode("utf-8"))

# # Send the multipart/form-data body
# conn.sendall(multipart_body.encode("utf-8"))