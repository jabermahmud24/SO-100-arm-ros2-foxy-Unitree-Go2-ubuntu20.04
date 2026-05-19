from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    xacro_file = PathJoinSubstitution([
        FindPackageShare('so_arm_100_description'),
        'urdf',
        'so_arm_100_5dof.urdf.xacro'
    ])

    controller_config = PathJoinSubstitution([
        FindPackageShare('so_arm_100_foxy_bringup'),
        'config',
        'ros2_controllers.yaml'
    ])

    robot_description = {
        'robot_description': ParameterValue(
            Command([
            '/opt/ros/foxy/bin/xacro',
            ' ',
            xacro_file
            ]),
            value_type=str
        )
    }

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        output='screen',
        parameters=[robot_description, controller_config]
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['arm_controller', '--controller-manager', '/controller_manager'],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        control_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner
    ])
