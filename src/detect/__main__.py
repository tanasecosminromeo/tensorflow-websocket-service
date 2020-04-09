## ## ## ## ## Detect Client App
## This will be ran for each model and will receive jobs from the web socket that will be stored in redis
from os import environ
PORT=8001
DEBUG=True if environ['DEBUG'] == "TRUE" else False

import sys
sys.path.append('/code/src')

from logger import get_logging
logging = get_logging('detect', DEBUG)

## Start app
import numpy as np
import time


from visualise import generateImage
from jobs import jobs

detectionId = 0

from tfsession import tf, labels
jobs.labels(labels)
logging.debug('Will detect the following categories '+str(labels))

ret = True
while (ret):
  job = jobs.get()
  detectionId += 1
  image_np = job.input()

  if image_np == None:
    job.result(["fail"])
    continue

  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
  image_np_expanded = np.expand_dims(image_np, axis=0)
  (boxes, scores, classes, num_detections) = tf.run(image_np_expanded)

  detections = []
  for index, score in enumerate(np.squeeze(scores)):
    if score > 0.1:
      detections.append([
        '%.4f' %(float(score)), #score in percentage
        np.squeeze(boxes)[index].tolist(), #bounding box
        int(np.squeeze(classes).astype(np.int32)[index]) #classId
        ])

  if job.withImage:
    image_base64 = generateImage(
      image_np,
      np.squeeze(boxes),
      np.squeeze(classes).astype(np.int32),
      np.squeeze(scores),
      labels,
      use_normalized_coordinates=True,
      line_thickness=8)

    #Store Detection in Redis
    job.result(["ok", detectionId, detections, str(image_base64)])
  else:
    image_base64 = ""
    #Store Detection in Redis
    job.result(["ok", detectionId, detections])

  logging.debug(
    "Job #%d: %s (%s)" % (detectionId, detections, "with-image" if job.withImage else "without-image")
  )
  time.sleep(jobs.cooldown())