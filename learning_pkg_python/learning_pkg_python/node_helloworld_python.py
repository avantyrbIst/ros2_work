#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node     # ← класс Node из модуля rclpy.node
import time

class HelloWorldNode(Node):     # ← с большой буквы N
    def __init__(self, name):
        super().__init__(name)  # ← super() со скобками, а не super.
        while rclpy.ok():
            self.get_logger().info("Hello World test")
            time.sleep(0.5)

def main(args=None):
    rclpy.init(args=args)
    node = HelloWorldNode("node_helloworld_class")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()