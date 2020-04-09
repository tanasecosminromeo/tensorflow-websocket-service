import logging, cv2
logger = logging.getLogger(__name__)

class streamClass:
    def __init__(self):
        self.streams = {}

    def read(self, job):
        ###Todo: Clear the stream if not used for a while (30sec???)
        if job.data not in self.streams:
            logger.debug(
                "Open stream #%s requested by job %d" % (job.data, job.id)
            )
            self.streams[job.data] = cv2.VideoCapture(job.data)

        ret, image = self.streams[job.data].read()

        if ret == False:
            logger.warning(
                "Steam %s requested by job #%d may be off" % (job.data, job.id)
            )

            return None

        return image

streams = streamClass()