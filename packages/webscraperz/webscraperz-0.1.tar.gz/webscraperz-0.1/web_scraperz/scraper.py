import os
# import websocket
import sys
from . import webpagedownload
url = "https://www.google.com"
def scraper():
    webpagedownload.webdownload(url)  #web page data raw download 