import re
from Http import *
from server import *
from udp_server import recieveFromClient

def parse_request(request_string):
    # Define the regex pattern
    pattern = r'^httpfs(?:\s+-v)?(?:\s+-p\s+(\d+))?(?:\s+-d\s+(\S+))?$'
    
    # Match the request string against the pattern
    match = re.match(pattern, request_string)
    
    if match:
        port = match.group(1) or '8080'  # Default port is 8080
        path = match.group(2) or 'data'  # Default directory is the current directory
        recieveFromClient(8007)
        return True
    else:
        return False

# Keep getting input and processing it until the program is exited
while True:
    request = input("Enter your request (or type 'exit' to quit): ")
    if request.lower() == 'exit':
        break
    bol = parse_request(request)
    if bol:
        print("Good request!")
    else:
        print("Invalid request format!")

#httpfs -v -p 8080 -d data
#httpfs -v -p 8080 -d data/sub1

