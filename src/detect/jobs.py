# This will manage jobs and store them using the redis storage module
from storage import store
from streams import streams
import logging 
logger = logging.getLogger(__name__)

class jobs:
    def __init__():
        this.jobs = {}
    
    def labels(labels):
        store.set('joblabels', labels)

    def get():
        logger.debug('getjob')
        
        return job("yassss", 1, 'stream', 'http://192.168.100.67:8000/stream.mjpg', True)
    
    #After each job, it's stop and breath for a second.
    ###Todo: Make this configurable via redis
    def cooldown():
        return 1

class job:
    def __init__(self, client, id, type, data, withImage):
        self.client = client
        self.id = id
        self.type = type 
        self.data = data
        self.withImage = withImage

    def input(self):
        print(streams, self)
        return streams.read(self)

    def result(self, data):
        logger.debug('job.result')
        store.set('jobid', data)