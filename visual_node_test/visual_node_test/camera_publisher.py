#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')

        # Публикуем в /camera/image_raw с QoS для сенсорных данных (best_effort)
        self.pub = self.create_publisher(
            Image, '/camera/image_raw', qos_profile_sensor_data)

        # Открываем камеру (0 — встроенная/первая; можно указать /dev/videoX)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error('Не удалось открыть камеру')
            raise RuntimeError('camera open failed')

        # Настраиваем разрешение и FPS (некоторые камеры игнорируют — это нормально)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.bridge = CvBridge()
        fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        period = 1.0 / fps
        self.timer = self.create_timer(period, self.tick)
        self.get_logger().info(f'Публикую кадры в /camera/image_raw с частотой ~{fps:.0f} Гц')

    def tick(self):
        ok, frame = self.cap.read()
        if not ok:
            self.get_logger().warn('Не удалось получить кадр')
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'
        self.pub.publish(msg)

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()