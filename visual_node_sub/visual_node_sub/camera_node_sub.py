#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraViewer(Node):
    def __init__(self):
        super().__init__('camera_viewer')

        self.bridge = CvBridge()
        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.on_image, qos_profile_sensor_data)

        self.window = 'Camera Viewer'
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)

        self.last_frame = None
        # waitKey + imshow вызываем в главном потоке через таймер
        self.timer = self.create_timer(1.0 / 30.0, self.render)

        self.get_logger().info('Жду кадры из /camera/image_raw...')

    def on_image(self, msg: Image):
        try:
            self.last_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'cv_bridge: {e}')

    def render(self):
        if self.last_frame is None:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                raise KeyboardInterrupt
            return
        cv2.imshow(self.window, self.last_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            raise KeyboardInterrupt

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()