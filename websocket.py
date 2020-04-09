## ## ## ## ## WebSocket Main App
from os import environ
PORT=8001
DEBUG=True if environ['DEBUG'] == "TRUE" else False

from src.logger import get_logging
logging = get_logging('websocket', DEBUG)

## Start app
from SimpleWebSocketServer import SimpleWebSocketServer
from src.socket.socket import TFSocket

logging.info('Server starting on port ' + str(PORT) + ' exposed on ' + str(environ['WEBSOCKET_PORT']))
server = SimpleWebSocketServer('', PORT, TFSocket)
server.serveforever()