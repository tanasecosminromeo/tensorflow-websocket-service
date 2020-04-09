from os import environ, path
from http import server
import logging 
logger = logging.getLogger(__name__)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info("%s - - [%s] %s" % (self.address_string(),self.log_date_time_string(),format%args))

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/socket-port.js':
            content=("window.WEBSOCKET_PORT="+environ['WEBSOCKET_PORT']).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif path.exists('web'+self.path):
            file = open("web"+self.path, "r")
            extension = self.path.split(".")[-1]
            content = file.read().encode('utf-8')
            file.close()
            self.send_response(200)
            if extension == 'html':
                self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)
            self.end_headers()