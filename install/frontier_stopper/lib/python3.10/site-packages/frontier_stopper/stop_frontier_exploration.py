import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool

class FrontierController(Node):
    def __init__(self) -> None:
        super().__init__("FrontierController")
        self._sub = self.create_subscription(
            Bool, "shoe_detected", self.set_state, 10
        )
        self._pub = self.create_publisher(
            Bool, "explore/resume", 10
        )
        
    # when sandal detected, stop frontier exploration
    def set_state(self, msg: Bool) -> None:
        if msg.data == False:
            pub = Bool()
            pub.data = False
            self._pub.publish(pub)
            
def main():
    rclpy.init()
    node = FrontierController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
