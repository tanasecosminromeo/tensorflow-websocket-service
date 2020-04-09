## ## ## ## ## HTTPServer Main App
from os import environ
PORT=8000
DEBUG=True if environ['DEBUG'] == "TRUE" else False

from src.logger import get_logging
logging = get_logging('httpserver', DEBUG)

## Start app
import socketserver
from threading import Condition
from http import server

from src.httpserver.output import StreamingOutput
from src.httpserver.handler import StreamingHandler

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

logging.info('HTTP Server starting on port ' + str(PORT) + ' exposed on ' + str(environ['HTTP_PORT']))
address = ('', PORT)
server = StreamingServer(address, StreamingHandler)
server.serve_forever()