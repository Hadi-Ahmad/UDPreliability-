import argparse
from Http import *

getParser = argparse.ArgumentParser()
getParser.add_argument("--host", help="server host", default="httpbin.org")
getParser.add_argument("--port", help="server port", type=int, default=80)
getParser.add_argument("--resource", help="server resource", type=str, default = "/")
getParser.add_argument("--params", help="server params", type=object, default = None)
getParser.add_argument("--headers", help="server headers", type=object, default=None)
getParser.add_argument("--verbosity", help="server verbosity", type=bool, default=None)

getargs = getParser.parse_args()


postParser = argparse.ArgumentParser()
postParser.add_argument("--host", help="server host", default="ptsv3.com")
postParser.add_argument("--port", help="server port", type=int, default=80)
postParser.add_argument("--resource", help="server resource", type=str, default="/")
postParser.add_argument("--params", help="server params", type=str, default="")
postParser.add_argument("--files", help="server files", type=str, default=None)
postParser.add_argument("--headers", help="server headers", type=object, default=None)
postParser.add_argument("--verbosity", help="server verbosity", type=bool, default=None)
# postParser.add_argument("--contentType", help="server content type", type=str, default=None)
# postParser.add_argument("--connection", help="server connection", type=str, default=None)

postargs = postParser.parse_args()

# getHTTP(getargs.host,   getargs.port,   "/status/418", getargs.params,  getargs.headers,False)
# getHTTP(getargs.host, getargs.port, "/get", {"assignment" : "1", "course": "networking"}, getargs.headers,True)
getHTTP(getargs.host, getargs.port, "/status/500", getargs.params, {'Connection':'close','Content-Type':'text/html'},False)
# postHTTP(postargs.host, postargs.port, "/t/22/","oct1", postargs.files,postargs.headers,False)
# postHTTP("httpbin.org", postargs.port, "/post", {"test": True}, postargs.files, {'Connection':'close'},True)
# postHTTP("httpbin.org", postargs.port, "/post", {"assignment":1}, postargs.files ,postargs.headers,False)
# postHTTP("httpbin.org", postargs.port, "/post", "Sept24",  postargs.files ,{'Connection':'close'},True)
# postHTTP("httpbin.org", postargs.port, "/post", postargs.params, "./t1.txt", postargs.headers,False)
# postHTTP("httpbin.org", postargs.port, "/status/301", postargs.params,  postargs.files ,postargs.headers,True)
getHTTP("httpbin.org",   getargs.port,   "/status/301" , getargs.params,  getargs.headers,True)


# link1 = str(httpc get -v 'http://httpbin.org/get?course=networking&assignment=1')
# link2 = httpc post -h Content-Type:application/json --d '{"Assignment": 1}' http://httpbin.org/post
# link3 = str(httpc post -h Connection:close -h Content-Type:text/html -d Exect http://ptsv3.com/t/22/)
# link4 = str(httpc get -v http://httpbin.org/status/418)
# link5 = str(httpc post -v -f ./t1.txt http://httpbin.org/post)
# link6 = str(httpc get -v -h Cookie:sessionid=abcdef123456 http://httpbin.org/get)
