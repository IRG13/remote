import rclpy
from std_msgs.msg import Bool  # Adjust the message type based on your topic

def callback(msg):
    print(f"Received message: {msg.data}")
    # Add your custom logic here based on the received message
    # You may set a flag or perform some other action to indicate the condition is met
    rclpy.shutdown()

def wait_for_topic():
    rclpy.init()

    node = rclpy.create_node('wait_for_topic_node')

    # Replace 'your/ros/topic' and std_msgs.msg.String with the actual topic and message type
    subscriber = node.create_subscription(Bool, 'bot_started', callback, 10)

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    wait_for_topic()
