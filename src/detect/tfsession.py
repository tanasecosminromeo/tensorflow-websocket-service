import tensorflow.compat.v1 as tensorflow
from model import category_index, load_detection_graph, MODEL_NAME

detection_graph = load_detection_graph(tensorflow)

class tf:
    # Running the tensorflow session
    def run(image):
        with detection_graph.as_default():
            with tensorflow.Session(graph=detection_graph) as sess:
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

                # Each box represents a part of the image where a particular object was detected.
                boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                scores = detection_graph.get_tensor_by_name('detection_scores:0')
                classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                # Actual detection.
                return sess.run(
                [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image})

labels = category_index