import argparse
from Http import *
from urllib.parse import urlparse, parse_qs
from udp_client import sendToServer

curlParser = argparse.ArgumentParser()

# curlParser.add_argument("--method", help="type of request", required=True)
# curlParser.add_argument("--verbose", help = "verbose request",default=None, required=False)
# curlParser.add_argument("--headers1", help = "Content-Type", default=None, required=False)
# curlParser.add_argument("--headers2", help = "Connection", default=None, required=False)
# curlParser.add_argument("--inline", help = "inline data", default=None, required=False)
# curlParser.add_argument("--file", help = "file data", default=None, required=False)
# curlParser.add_argument("--URL", help = "Content-Type", required=True)

request = None
isVerbose = False
inlineData = None
fileValue = None
URL = None
headers_dict = {}
textToWrite = ""
fileNameToWrite = ""
postHelpString = """
usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL
Post executes a HTTP POST request for a given URL with inline data or from
file.
 -v Prints the detail of the response such as protocol, status,
and headers.
 -h key:value Associates headers to HTTP Request with the format
'key:value'.
 -d string Associates an inline data to the body HTTP POST request.
 -f file Associates the content of a file to the body HTTP POST
request.
Either [-d] or [-f] can be used but not both."""

getHelpString = """
usage: httpc get [-v] [-h key:value] URL
Get executes a HTTP GET request for a given URL.
 -v Prints the detail of the response such as protocol, status,
and headers.
 -h key:value Associates headers to HTTP Request with the format
'key:value'."""


while True:
    command = input()
    result = command.split()
    request = result[1]

    if 'help' in result and 'get' in result:
        print(getHelpString)
        print("\n")
        continue
    if 'help' in result and 'post' in result:
        print(postHelpString)
        print("\n")
        continue
    if 'exit' in result:
        break
    elif 'post' in result and '-d' in result and '-f' in result:
        print("error\n")
    elif 'get' in result and '-d' in result:
        print ("error\n")
    elif 'get' in result and '-f' in result:
        print ("error\n")
    else:
        if '-v' in result:
            isVerbose = True
        if '-h' in result:
            for index, value in enumerate(result):
             if value == '-h':
                singleHeader = result[index + 1].split(":")
                headers_dict[singleHeader[0]] = singleHeader[1]
        if '-d' in result or '--d' in result:
            for index, value in enumerate(result):
                if value == '-d' or value == '--d':
                    inlineData = result[index + 1]
        if '-f' in result:
            for index, value in enumerate(result):
                if value == '-f':
                    fileValue = result[index + 1]
        if '-o' in result:
            for index, value in enumerate(result):
                if value == '-o':
                    fileNameToWrite = result[index + 1]
        for index, value in enumerate(result):
            if value.startswith("http") or value.startswith("'http") or value.startswith('"http') and value != "httpc":
                if(value.startswith("'http")) or value.startswith('"http'):
                    value = value[1:-1]
                URL = value
        # print(request)
        if(isVerbose is False):
            isVerbose = None
        # print(isVerbose)
        if(len(headers_dict) == 0):
            headers_dict = None
        # print(headers_dict)
        if(inlineData == "Empty"):
            inlineData = None
        # print(inlineData)
        if(fileValue == "Empty"):
            fileValue = None
        # print("DATA:", fileValue or inlineData)
        # print(URL)
        parsed_url = urlparse(URL)
        host = parsed_url.netloc  # "www.example.com"
        path = parsed_url.path  # "/path/to/resource"
        query = parsed_url.query  # "param1=value1&param2=value2"
        query_parameters = parse_qs(query)
        query_parameters_dict = {key: values[-1] for key, values in query_parameters.items()}
        if(request=="get"):
            print("Sending get request...")
            request = getHTTP(host,41830,path,query_parameters_dict,headers_dict,isVerbose)
            response = sendToServer(host, 41830, request, "localhost", 3000)
        elif(request=="post"):
            print("Posting request...")
            request = postHTTP(host,41830,path,inlineData,fileValue,headers_dict,isVerbose)
            response = sendToServer(host, 41830, request, "localhost", 3000)
        request = None
        isVerbose = False
        inlineData = None
        fileValue = None
        textToFIle=""
        fileNameToWrite=""
        URL = None
        headers_dict = {}

#httpc get -v 'http://localhost/'

#httpc get -v 'http://localhost/sub1/sub2'
#httpc get -v 'http://localhost/test.txt'
#httpc post -v -d hellohadi 'http://localhost/boo.html'
#httpc post -v -d secondterminaltestdemo2 'http://localhost/boo.html'
#httpc post -v -d secondterminaltestdemo2 'http://localhost/createtxt.txt' 
#httpc get -v 'http://localhost/..'  
#httpc get -v 'http://localhost/sub1/zzzzzz'



    










    





