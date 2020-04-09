##Todo: This will be useful to close models if not un used
# Useful to handle killing tensorflow process
# from src.helpers import kill_all_child
# import atexit
# atexit.register(kill_all_child)


class TFHandle:
    def __call__(self, socket):
        print('test')

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