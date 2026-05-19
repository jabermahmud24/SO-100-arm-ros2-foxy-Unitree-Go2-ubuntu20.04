#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


JOINT_NAMES = [
    'Shoulder_Rotation',
    'Shoulder_Pitch',
    'Elbow',
    'Wrist_Pitch',
    'Wrist_Roll',
    'Gripper',
]


class ArmCommander(Node):
    def __init__(self):
        super().__init__('simple_arm_commander')
        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            '/arm_controller/follow_joint_trajectory'
        )

    def close(self):
        if self.client is not None:
            self.client.destroy()
            self.client = None

    def send_goal(self, positions, duration_sec=2.0):
        if not self.client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Action server not available.')
            return False

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = JOINT_NAMES

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start = Duration(
            sec=int(duration_sec),
            nanosec=int((duration_sec - int(duration_sec)) * 1e9)
        )

        goal_msg.trajectory.points = [point]

        self.get_logger().info(f'Sending: {positions}')
        future = self.client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error('Goal rejected.')
            return False

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)

        result = result_future.result()
        if result is None:
            self.get_logger().error('No result received.')
            return False

        self.get_logger().info('Pose completed.')
        return True


def main():
    rclpy.init()
    node = ArmCommander()

    # Put the poses here
    poses = [
            [0.73067, -0.147, -0.0612, -1.1259, -1.6091, 0.1],   # Pose 1
            [0.00, -2.0, 1.512, -1.1259, -1.6091, 0.5],  # Pose 2],   
            [0.00, -3.0, 2.2, 0.0, -1.0, 0.0]# Pose 3
    ]

    for i, pose in enumerate(poses, start=1):
        node.get_logger().info(f'Executing pose {i}')
        ok = node.send_goal(pose, duration_sec=5.0)
        if not ok:
            node.get_logger().error(f'Failed at pose {i}')
            break
    
    node.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
