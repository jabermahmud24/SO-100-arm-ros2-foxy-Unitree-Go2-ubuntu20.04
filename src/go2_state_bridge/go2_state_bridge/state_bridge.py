#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from unitree_go.msg import LowState
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped, TwistStamped
from std_msgs.msg import Float32MultiArray


class Go2StateBridge(Node):
    def __init__(self):
        super().__init__('go2_state_bridge')

        self.declare_parameter('lowstate_topic', '/lf/lowstate')
        self.declare_parameter('odom_topic', '/uslam/localization/odom')
        self.declare_parameter('motor_count', 20)

        lowstate_topic = self.get_parameter('lowstate_topic').value
        odom_topic = self.get_parameter('odom_topic').value
        self.motor_count = int(self.get_parameter('motor_count').value)

        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.pose_pub = self.create_publisher(PoseStamped, '/go2/base_pose', 10)
        self.twist_pub = self.create_publisher(TwistStamped, '/go2/base_twist', 10)
        self.foot_force_pub = self.create_publisher(Float32MultiArray, '/go2/foot_force', 10)

        self.low_sub = self.create_subscription(
            LowState,
            lowstate_topic,
            self.lowstate_callback,
            qos_profile_sensor_data
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            odom_topic,
            self.odom_callback,
            qos_profile_sensor_data
        )

        self.get_logger().info(
            f'Listening to lowstate={lowstate_topic}, odom={odom_topic}'
        )

    def lowstate_callback(self, msg: LowState):
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = [f'motor_{i}' for i in range(self.motor_count)]
        js.position = [msg.motor_state[i].q for i in range(self.motor_count)]
        js.velocity = [msg.motor_state[i].dq for i in range(self.motor_count)]
        js.effort = [msg.motor_state[i].tau_est for i in range(self.motor_count)]
        self.joint_pub.publish(js)

        ff = Float32MultiArray()
        ff.data = [float(x) for x in msg.foot_force]
        self.foot_force_pub.publish(ff)

        self.get_logger().debug(
            f'power_v={msg.power_v:.2f}, power_a={msg.power_a:.2f}'
        )

    def odom_callback(self, msg: Odometry):
        pose_msg = PoseStamped()
        pose_msg.header = msg.header
        pose_msg.pose = msg.pose.pose
        self.pose_pub.publish(pose_msg)

        twist_msg = TwistStamped()
        twist_msg.header = msg.header
        if msg.child_frame_id:
            twist_msg.header.frame_id = msg.child_frame_id
        twist_msg.twist = msg.twist.twist
        self.twist_pub.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)
    node = Go2StateBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
