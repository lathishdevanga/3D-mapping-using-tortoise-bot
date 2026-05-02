import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from ros_gz_interfaces.srv import SetEntityPose

class IMUToGazebo(Node):
    def __init__(self):
        super().__init__('imu_to_gazebo')

        # Subscribe to IMU
        self.sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        # Service client to move entity
        self.cli = self.create_client(SetEntityPose, '/world/default/set_pose')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Gazebo service...')

        self.get_logger().info("IMU → Gazebo bridge started")

    def imu_callback(self, msg):
        req = SetEntityPose.Request()
        req.name = "imu_box"
        req.pose.position.x = 0.0
        req.pose.position.y = 0.0
        req.pose.position.z = 0.5
        req.pose.orientation = msg.orientation
        self.cli.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    node = IMUToGazebo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()