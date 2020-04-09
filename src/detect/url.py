import urllib.request
import logging

logger = logging.getLogger(__name__)

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def getDataFromURL(url):
    opener = AppURLopener()
    response = opener.open(url)

    return response