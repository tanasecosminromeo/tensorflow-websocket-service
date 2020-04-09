import logging
from logging.handlers import RotatingFileHandler
from logging import handlers

def get_logging(app_name, DEBUG):
    LOGFILE = '/code/var/logs/'+app_name+'.log'

    log = logging.getLogger('')
    log.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    format = logging.Formatter("%(asctime)s: %(name)s.%(levelname)s - %(message)s")

    fh = handlers.RotatingFileHandler(LOGFILE, maxBytes=(1048576*5), backupCount=7)
    fh.setFormatter(format)
    log.addHandler(fh)

    if DEBUG:
        import sys
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(format)
        log.addHandler(ch)

    return logging
