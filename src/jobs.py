# This will manage jobs and store them using the redis storage module
import sys 
sys.path.append('/code/src')

from storage import store
from detect.streams import streams
from detect.url import getDataFromURL
import logging, base64, cv2, numpy as np

logger = logging.getLogger(__name__)
class jobs:
    def inQue():
        return store.llen('que')

    def inQue():
        return store.llen('results')
    
    ##Todo: These need to be specific to each mode;
    def labels(labels=None):
        if labels == None:
            return store.get('joblabels')
        else:
            store.set('joblabels', labels)

    def result():
        if store.llen('results') == 0:
            return None
        logger.debug('getjob result')
        [client, id, data] = store.lpop('results')

        return jobResult(client, id, data)
    def get():
        if store.llen('que') == 0:
            return None
        logger.debug('getjob')
        
        [client, id, type, data, withImage] = store.lpop('que')

        return job(client, id, type, data, withImage)
    
    #After each job, it's stop and breath for a second.
    ###Todo: Make this configurable via redis
    ###Todo: Lower this after testing
    def cooldown():
        return 0.01

    #If no jobs are found check again in
    ###Todo: Make this configurable via redis
    def recheck():
        return 1

class jobResult:
    def __init__(self, client, jobId, data, finished=False):
        self.client = client
        self.jobId = jobId
        self.data = data
        self.finished = finished

class job:
    def __init__(self, client, id, type, data, withImage):
        self.client = client
        self.id = id
        self.type = type 
        self.data = data
        self.withImage = withImage
    
    def send(self):
        store.rpush('que', [self.client, self.id, self.type, self.data, self.withImage])

    def input(self):
        try:
            if self.type == 'stream':
                return streams.read(self)
            elif self.type == 'base64':
                nparr = np.fromstring(base64.b64decode(self.data), np.uint8)
                return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            elif self.type == 'url':
                resp = getDataFromURL(self.data)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                return cv2.imdecode(image, cv2.IMREAD_COLOR)
            else:
                error = "Input type %s requested by job #%d is unsupported" % (self.type, self.id)
        except:
            error = "Cannot use input %s for job #%d - %s: %s " % (self.type, self.id, sys.exc_info()[0], sys.exc_info()[1])

        logger.critical(error)
        self.save(["fail", error])
        return None

    def save(self, data):
        logger.debug('job.save')

        store.rpush('results', [self.client, self.id, data])