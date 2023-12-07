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

        self.declare_parameter("model", "/home/arms/turtlebot3_ws/src/shoe_detector/shoe_detector/sandals.pt") 
        model = self.get_parameter(
            "model").get_parameter_value().string_value

        self.declare_parameter("device", "cuda:0")
        self.device = self.get_parameter(
            "device").get_parameter_value().string_value

        self.declare_parameter("threshold", 0.81)
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
        self._pub2 = self.create_publisher(
            Bool, "explore/resume", 10
        )

        self._srv = self.create_service(SetBool, "enable", self.enable_cb)
        self.sandaldetected = False

        self.pd = 0
        self.tempdet = 0

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
                show=True 
            )
            results: Results = results[0].cuda()
 
            pub = Bool()
            self.tempdet = 0
            for r in results:
                if r.boxes:
                    self.tempdet = 1
            # If sandal detected more than 4 instances
            if self.tempdet:
                self.pd += 1
            else:
                if self.pd > 0:
                     self.pd -= 1

            if self.pd > 4:
                self.pd = 0
                pub.data = False
                self._pub.publish(pub)
                self._pub2.publish(pub) # publish to /explore/resume false to stop exploration
                self.sandaldetected = False
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
