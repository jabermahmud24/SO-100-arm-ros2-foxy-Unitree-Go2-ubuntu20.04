import math
import time
from typing import List, Optional

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory

import serial


class FollowerArmHardware:
    """
    Replace the internals of this class with your real arm protocol.
    The ROS side should stay almost unchanged.
    """

    def __init__(self, port: str, baudrate: int, joint_count: int):
        self.port = port
        self.baudrate = baudrate
        self.joint_count = joint_count
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=0.05)
        time.sleep(2.0)

        # Last known positions in radians
        self._last_positions = [0.0] * joint_count

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def rad_to_hw(self, joint_index: int, rad: float) -> int:
        """
        Example conversion.
        Replace this with your real servo-unit mapping.
        """
        deg = math.degrees(rad)

        # Example: 0..4095 ticks over 0..360 deg
        ticks = int((deg % 360.0) / 360.0 * 4095.0)
        return max(0, min(4095, ticks))

    def hw_to_rad(self, joint_index: int, value: int) -> float:
        deg = (float(value) / 4095.0) * 360.0
        return math.radians(deg)

    def send_joint_positions(self, joint_positions_rad: List[float]):
        """
        Replace packet format below with your real controller packet.
        """
        if len(joint_positions_rad) != self.joint_count:
            raise ValueError("Wrong joint count")

        cmd_vals = [self.rad_to_hw(i, q) for i, q in enumerate(joint_positions_rad)]

        # Example ASCII packet:
        # SET 1000 2100 1900 2048 1500\n
        packet = "SET " + " ".join(str(v) for v in cmd_vals) + "\n"
        self.ser.write(packet.encode("utf-8"))

        # Keep local copy in case feedback is unavailable
        self._last_positions = joint_positions_rad[:]

    def read_joint_positions(self) -> List[float]:
        """
        Replace this with real feedback parsing.
        If your controller cannot return feedback yet,
        return last commanded positions temporarily.
        """
        # Example:
        # controller replies: POS 1000 2100 1900 2048 1500
        self.ser.write(b"GET\n")
        line = self.ser.readline().decode("utf-8", errors="ignore").strip()

        if line.startswith("POS "):
            try:
                vals = [int(x) for x in line.split()[1:]]
                if len(vals) == self.joint_count:
                    self._last_positions = [self.hw_to_rad(i, v) for i, v in enumerate(vals)]
            except Exception:
                pass

        return self._last_positions[:]


class FollowerArmBridge(Node):
    def __init__(self):
        super().__init__("follower_arm_bridge")

        self.declare_parameter("port", "/dev/ttyACM0")
        self.declare_parameter("baudrate", 115200)
        self.declare_parameter("joint_names", ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"])
        self.declare_parameter("publish_rate_hz", 20.0)

        self.port = self.get_parameter("port").value
        self.baudrate = int(self.get_parameter("baudrate").value)
        self.joint_names = list(self.get_parameter("joint_names").value)
        self.publish_rate_hz = float(self.get_parameter("publish_rate_hz").value)

        self.hw = FollowerArmHardware(
            port=self.port,
            baudrate=self.baudrate,
            joint_count=len(self.joint_names),
        )

        self.joint_state_pub = self.create_publisher(JointState, "/joint_states", 10)

        self.pos_sub = self.create_subscription(
            Float64MultiArray,
            "/position_controller/commands",
            self.position_cmd_cb,
            10,
        )

        self.traj_sub = self.create_subscription(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            self.trajectory_cmd_cb,
            10,
        )

        self.timer = self.create_timer(1.0 / self.publish_rate_hz, self.publish_joint_states)

        self.get_logger().info(f"Follower arm bridge started on {self.port} @ {self.baudrate}")

    def position_cmd_cb(self, msg: Float64MultiArray):
        if len(msg.data) != len(self.joint_names):
            self.get_logger().warn(
                f"Expected {len(self.joint_names)} joints, got {len(msg.data)}"
            )
            return

        self.hw.send_joint_positions(list(msg.data))

    def trajectory_cmd_cb(self, msg: JointTrajectory):
        if not msg.points:
            return

        point = msg.points[-1]
        if len(point.positions) != len(self.joint_names):
            self.get_logger().warn(
                f"Expected {len(self.joint_names)} trajectory positions, got {len(point.positions)}"
            )
            return

        # For a minimal driver, just take the final point and send it immediately.
        self.hw.send_joint_positions(list(point.positions))

    def publish_joint_states(self):
        positions = self.hw.read_joint_positions()

        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = self.joint_names
        js.position = positions
        js.velocity = [0.0] * len(self.joint_names)
        js.effort = [0.0] * len(self.joint_names)

        self.joint_state_pub.publish(js)

    def destroy_node(self):
        try:
            self.hw.close()
        except Exception:
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = FollowerArmBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
