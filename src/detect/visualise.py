#This will be useful if we want to return an actual image
from utils import visualization_utils as vis_util
from base64 import b64encode
import cv2, logging
logger = logging.getLogger(__name__)

def generateImage(
    image,
    boxes,
    classes,
    scores,
    category_index,
    instance_masks=None,
    keypoints=None,
    use_normalized_coordinates=False,
    max_boxes_to_draw=20,
    min_score_thresh=.5,
    agnostic_mode=False,
    line_thickness=4):

    logger.debug('Generating image')
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        boxes,
        classes,
        scores,
        category_index,
        instance_masks,
        keypoints,
        use_normalized_coordinates,
        max_boxes_to_draw,
        min_score_thresh,
        agnostic_mode,
        line_thickness)
    
    #Encode image
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    logger.debug('Encoding image')
    _, buffer = cv2.imencode('.jpg', image, encode_param)
    return str(b64encode(buffer))