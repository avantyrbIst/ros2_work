import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from ultralytics import YOLO
class CameraNodeHailo(Node):
    def __init__(self, name):
        super().__init__(name)
        self.camera_sub = self.create_subscription(
            Image, '/uav1/rpi_camera_front/image_raw', self.camera_callback, 10)
        self.bridge = CvBridge()
        self.model = YOLO("/home/ros2/ros2_ws/src/video_node/video_node/yolov8n.pt")
    def camera_callback(self, msg):
        self.get_logger().info('Received image')
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = model(frame, classes=[0], verbose=False)
        annotated = results[0].plot()
        cv2.imshow('Camera',annotated)
        cv2.waitKey(1)

    def destroy_node(self):
        cv2.destroyAllWindows()
        return super().destroy_node()
        
def main(args=None):
    rclpy.init(args=args)
    node = CameraNodeHailo('camera_node')
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == '__main__':
    main()
