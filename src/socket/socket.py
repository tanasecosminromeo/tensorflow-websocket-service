import hashlib, json, logging
logger = logging.getLogger(__name__)

from SimpleWebSocketServer import WebSocket
from src.socket.handle import TFHandle

from src.jobs import job, jobs

clients = []
import subprocess

from src.socket.command import TFCommand, PrepareResult

class TFSocket(WebSocket):
   def send(self, command, data, error=False):
      self.sendMessage(json.dumps([command.id, command.action, "ok" if not error else "error", data]))
   
   def sendJobResults(self):
      while True:
         result = jobs.result()

         if result != None:
            for c in clients:
               if c.hash == result.client:
                  command = PrepareResult(result)
                  c.send(command, result.data)
         else:
            break

   def handleMessage(self):
      command = TFCommand(self.data)
      if command.action == 'ping':
         self.send(command, 'pong')
      elif command.action == 'labels':
         self.send(command, jobs.labels())
      elif command.action == 'detect':
         [type, data] = command.parameters

         if type not in ['url', 'base64', 'stream']:
            self.send(command, "invalid type %s" % str(type), True)
         
         try:
            job(self.hash, command.id, type, data, False).send()
         except:
            logging.debug(
               "Error processing command #%d from %s - %s %s" % [command.id, self.hash, sys.exc_info()[0], sys.exc_info()[1]]
            )

      self.sendJobResults()
      
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
   
   def clients(self):
      return clients