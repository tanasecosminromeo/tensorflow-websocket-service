# This module wil read the parameters for this detection
import sys, logging 
logger = logging.getLogger(__name__)

if len(sys.argv) < 2:
  logging.critical('You must specify a MODEL_NAME (PS: The logic behind this is not working yet, but still, better to be prepared than not to be prepared')
  sys.exit()

MODEL_NAME=sys.argv[1]