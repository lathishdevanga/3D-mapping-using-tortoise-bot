import rclpy
from rclpy.node import Node
import serial
import math

from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion, TransformStamped
from tf2_ros import TransformBroadcaster


class IMUSerialNode(Node):

    def __init__(self):
        super().__init__('imu_serial_node')

        # Parameters
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baud", 115200)

        port = self.get_parameter("port").value
        baud = self.get_parameter("baud").value

        # Serial connection
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            self.get_logger().info(f"Connected to {port} @ {baud}")
        except Exception as e:
            self.get_logger().error(f"Serial connection failed: {e}")
            exit()

        # Publisher
        self.pub = self.create_publisher(Imu, "imu/data", 10)

        # TF broadcaster
        self.br = TransformBroadcaster(self)

        # Timer loop (100 Hz)
        self.timer = self.create_timer(0.01, self.read_serial)

        self.get_logger().info("IMU Serial Node Started")


    def read_serial(self):

        try:
            line = self.ser.readline().decode(errors='ignore').strip()
        except:
            return

        parts = line.split()
        if len(parts) != 4:
            return

        try:
            qw, qx, qy, qz = map(float, parts)
        except:
            return

        # Normalize quaternion
        norm = math.sqrt(qw*qw + qx*qx + qy*qy + qz*qz)
        if norm == 0:
            return

        qw /= norm
        qx /= norm
        qy /= norm
        qz /= norm

        # ---------- IMU MESSAGE ----------
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"

        msg.orientation = Quaternion(x=qx, y=qy, z=qz, w=qw)

        # (optional but recommended)
        msg.orientation_covariance[0] = 0.002
        msg.orientation_covariance[4] = 0.002
        msg.orientation_covariance[8] = 0.002

        self.pub.publish(msg)

        # ---------- TF TRANSFORM ----------
        t = TransformStamped()

        t.header.stamp = msg.header.stamp
        t.header.frame_id = "world"
        t.child_frame_id = "imu_link"

        t.transform.rotation = msg.orientation

        self.br.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = IMUSerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()