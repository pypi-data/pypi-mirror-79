import sys
import urllib.request
weburl = "https://www.google.com"
def webdownload(weburl):
    print ("It's work")
    webpage = None;
    webpage  = urllib.request.urlopen(weburl)
    conn = None;
    conn = webpage.read()
    print (conn)
    return conn
