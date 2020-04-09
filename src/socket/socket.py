import hashlib, json, logging, redis
logger = logging.getLogger(__name__)

from SimpleWebSocketServer import WebSocket
from src.socket.command import TFCommand

store = redis.Redis()

clients = []
import subprocess

class TFSocket(WebSocket):
   def handleMessage(self):
      command = TFCommand(self.data)
      print(command.action)
      # command = TFCommand(self.data)
      # if self.data == "image":
      #    redis_data = store.get(self.clientHash+"-detection")
      #    if redis_data != None:
      #       data = json.loads(redis_data)
      #       # print('sent image', data)
      #       self.sendMessage(json.dumps(['ok', 'image', data]))
      #       #self.sendMessage(json.dumps(['ok', 'image', clientProc[self.clientHash], json.loads(store.get(self.clientHash+"-detection")) ] ))
      #    else:
      #       print('loading')
      #       self.sendMessage(json.dumps(['loading']))
      # elif self.data == "label":
      #    redis_data = store.get(self.clientHash+"-categories")
      #    if redis_data != None:
      #       data = json.loads(redis_data)
      #       print('sent label', data)
      #       self.sendMessage(json.dumps(['ok', 'label', data]))
      #    else:
      #       self.sendMessage(json.dumps(['loading']))
      # elif self.data == "start-stream":
      #    proc = subprocess.Popen(["/usr/bin/python3", "/code/detect.py", self.clientHash, "http://192.168.100.67:8000/stream.mjpg", "debug", "generate-image2"], stdin=None, stdout=subprocess.PIPE)
      #    clientProc[self.clientHash] = proc.pid
      # else:
      #    print('invalid command')
      #    self.sendMessage(json.dumps(['error', self.data, 'invalid command']))

   def handleConnected(self):
      sha_1 = hashlib.sha1()
      sha_1.update(json.dumps(self.address).encode('utf-8'))
      self.hash = sha_1.hexdigest()
      clients.append(self)
      logging.info(json.dumps(self.address)+' connected - Client Id '+str(self.hash))

   def handleClose(self):
      logging.info(json.dumps(self.address)+' closed')
      clients.remove(self)
      clientProc.remove(clientProc[self.hash])
      kill(clientProc[self.hash])