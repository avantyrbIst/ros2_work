from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

from ultralytics import YOLO

class UltralyticsNode(Node):
    """Run YOLO detection on ROS2 image messages."""

    def __init__(self):
        """Initialize the ROS2 node, model, and image interfaces."""
        super().__init__("ultralytics")
        self.bridge = CvBridge()
        self.model = YOLO("yolov8n_hailo_model")
        self.publisher = self.create_publisher(Image, "/ultralytics/detection/image", 5)
        self.create_subscription(Image, "/uav1/rpi_camera_front/image_raw", self.callback, qos_profile_sensor_data)

    def callback(self, message):
        """Publish the annotated camera frame."""
        image = self.bridge.imgmsg_to_cv2(message, desired_encoding="bgr8")
        annotated = self.model(image)[0].plot(show=False)
        self.publisher.publish(self.bridge.cv2_to_imgmsg(annotated, encoding="bgr8"))

def main(args=None):
    """Start the ROS2 node."""
    rclpy.init(args=args)
    node = UltralyticsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
