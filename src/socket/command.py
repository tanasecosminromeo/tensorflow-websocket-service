import logging, json, sys
logger = logging.getLogger(__name__)

class TFCommand():
    def __init__(self, jsonString):
        try:
            self.action, self.parameters, self.commandId = json.loads(jsonString)

            logger.debug(
                "Received command #%d %s (%s)" % (self.commandId, self.action, str(self.parameters))
            )
        except:
            logger.critical(str(sys.exc_info()[0])+' '+str(sys.exc_info()[1])+': '+str(jsonString))