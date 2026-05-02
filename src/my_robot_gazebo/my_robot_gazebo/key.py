import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import keyboard



class Key(Node):
    def __init__(self):
        super().__init__('key_processor')
        self.key_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.twist = Twist()

        while True:
  
            if keyboard.read_key() == "l":
                self.twist.linear.x = 5.0
            elif keyboard.read_key() == "k":
                self.twist.linear.x = -5.0
    





def main(args=None):
    rclpy.init(args=args)
    node = Key()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
