import psutil

def kill(proc_pid):
   process = psutil.Process(proc_pid)
   for proc in process.children(recursive=True):
      loggin.debug('Kill ', proc)
      proc.kill()


def kill_all_child():
   try: 
      kill(proc.pid)
   except:
      logging.debug('no child to kill')