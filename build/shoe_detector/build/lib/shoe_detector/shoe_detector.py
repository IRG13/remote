import rclpy
from rclpy.node import Node
import numpy as np

from cv_bridge import CvBridge

from ultralytics import YOLO
from ultralytics.engine.results import Results
from ultralytics.engine.results import Boxes

from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from std_srvs.srv import SetBool

#subscribes to /video0 and publishes to /shoe_detected

class ShoeDetectorNode(Node):
    
    def __init__(self) -> None:
        super().__init__("shoedetector_node")

        # Current model is just yolov8n.pt renamed as shoes.pt for testing, todo
        self.declare_parameter("model", "/home/arms/turtlebot3_ws/yolov8n.pt") 
        model = self.get_parameter(
            "model").get_parameter_value().string_value

        self.declare_parameter("device", "cuda:0")
        self.device = self.get_parameter(
            "device").get_parameter_value().string_value

        self.declare_parameter("threshold", 0.5)
        self.threshold = self.get_parameter(
            "threshold").get_parameter_value().double_value

        self.declare_parameter("enable", True)
        self.enable = self.get_parameter(
            "enable").get_parameter_value().bool_value
        
        self.cv_bridge = CvBridge()
        self.yolo = YOLO(model)
        self.yolo.fuse()

        self._sub = self.create_subscription(
            Image, "video0", self.shoe_detection,
            10
        )

        self._pub = self.create_publisher(Bool, 'shoe_detected', 10)

        self._srv = self.create_service(SetBool, "enable", self.enable_cb)
        self.sandaldetected = False

    def enable_cb(
        self,
        req: SetBool.Request,
        res: SetBool.Response
    ) -> SetBool.Response:
        self.enable = req.data
        res.success = True
        return res
    
    def shoe_detection(self, msg: Image) -> None:
        
        if self.enable:
            height = msg.height
            width = msg.width
            channel = msg.step//msg.width
            cv_image = np.reshape(msg.data, (height, width, channel))

#            cv_image = self.cv_bridge.imgmsg_to_cv2(msg)
            results = self.yolo.predict(
                source=cv_image,
                verbose=False,
                stream=False,
                conf=self.threshold,
                device=self.device,
                # show=True for debugging
            )
            results: Results = results[0].cuda()
 
            pub = Bool()
            ctr = 0
            for result in results:
                detection_count = result.boxes.shape[0]
                for i in range(detection_count):
                    cls = int(result.boxes.cls[i].item())
                    name = result.names[cls]
                    if name == "open":
                        print('Sandal detected')
                        self.sandaldetected = True

            # If sandal detected
            if self.sandaldetected:
                pub.data = False
                self._pub.publish(pub)

            # if nothing or shoe detected, just return True since theres no shoe
            else:
                pub.data = True
                self._pub.publish(pub)

def main():
    rclpy.init()
    node = ShoeDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()