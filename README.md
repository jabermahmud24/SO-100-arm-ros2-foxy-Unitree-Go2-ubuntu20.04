# SO-100 Arm ROS 2 Foxy Package for Unitree Go2 on Ubuntu 20.04

This repository provides a ROS 2 Foxy-compatible workspace for running the SO-100 / SO-ARM100 robotic arm on a Unitree Go2 robot running Ubuntu 20.04.

The original SO-100 ROS 2 package was developed for ROS 2 Humble. This repository adapts the package structure, dependencies, launch files, and hardware bringup workflow for ROS 2 Foxy and the Unitree Go2 onboard Ubuntu 20.04 environment.

---

## Acknowledgments

This repository is based on the original ROS 2 SO-100 arm repository by Bruk G.:

```text
https://github.com/brukg/SO-100-arm
```

The original repository provides the base ROS 2 package structure, robot description, launch files, controller configuration, and MoveIt/Gazebo-related setup.

This repository also includes/adapts the SO-100 hardware interface package:

```text
https://github.com/brukg/so_arm_100_hardware
```

The hardware interface provides ROS 2 Control support for the SO-100 arm, including serial communication with the physical robot and topic-based simulation support.

This version modifies and adapts the original work for:

- ROS 2 Foxy
- Ubuntu 20.04
- Unitree Go2 onboard computer
- Mounted SO-100 / SO-ARM100 arm operation

Credit is preserved to the original authors and repositories.

---

## Repository Status

This repository is intended for:

- Unitree Go2 onboard computer
- Ubuntu 20.04
- ROS 2 Foxy
- SO-100 / SO-ARM100 5-DOF arm with gripper
- Feetech-style serial servo hardware interface
- ROS 2 Control-based arm control

ROS 2 Foxy is an older ROS 2 distribution, but it is useful for the Unitree Go2 onboard Ubuntu 20.04 setup.

---

## Repository Structure

```text
SO-100-arm-ros2-foxy-Unitree-Go2-ubuntu20.04/
├── README.md
├── LICENSE
├── ACKNOWLEDGMENTS.md
├── .gitignore
├── src/
│   ├── SO-100-arm/
│   │   ├── so_arm_100/
│   │   ├── so_arm_100_bringup/
│   │   ├── so_arm_100_description/
│   │   └── so_arm_100_moveit_config/
│   │
│   ├── so_arm_100_hardware/
│   │   └── ROS 2 Control hardware interface for the SO-100 arm
│   │
│   ├── so_arm_100_foxy_bringup/
│   │   └── Minimal ROS 2 Foxy bringup package for physical hardware
│   │
│   ├── go2_state_bridge/
│   │   └── Optional Go2 state/odometry bridge package
│   │
│   └── follower_arm_driver/
│       └── Optional follower/control support package
│
└── scripts/
    └── arm_movement.py
```

The most important packages are:

| Package | Purpose |
|---|---|
| `so_arm_100_description` | URDF/Xacro robot description and meshes |
| `so_arm_100` | Main SO-100 package from the original ROS 2 implementation |
| `so_arm_100_bringup` | Original bringup/configuration package |
| `so_arm_100_moveit_config` | MoveIt configuration |
| `so_arm_100_hardware` | ROS 2 Control hardware interface for the physical SO-100 arm |
| `so_arm_100_foxy_bringup` | Foxy-specific launch/config files for Go2 hardware use |
| `go2_state_bridge` | Optional bridge for Unitree Go2 state/odometry topics |
| `follower_arm_driver` | Optional driver/control support package |
| `scripts/arm_movement.py` | Example Python script for sending arm trajectory goals |

---

## Main Modifications in This Fork

Compared with the original ROS 2 Humble repository, this version includes changes for:

- ROS 2 Foxy compatibility
- Ubuntu 20.04 support
- Unitree Go2 onboard computer setup
- Updated dependency handling for Foxy
- Foxy-compatible hardware launch workflow
- Integration of the SO-100 hardware interface package
- Example trajectory command script
- Repository organization as a workspace-style project with `src/` and `scripts/`

---

## Hardware Requirements

For the physical robot setup, you need:

- Unitree Go2 robot with Ubuntu 20.04 onboard computer
- ROS 2 Foxy installed on the Go2 computer
- SO-100 / SO-ARM100 robotic arm
- Feetech-compatible serial servos
- USB-to-serial servo adapter
- External power supply for the arm servos
- Correct mechanical mount for attaching the arm to the Go2 body

Important: Do not power the arm servos directly from the Go2 USB port. Use a proper external power supply for the servos.

---

## Software Requirements

Tested target environment:

```text
OS: Ubuntu 20.04
ROS 2: Foxy
Build system: colcon
Middleware: CycloneDDS or default ROS 2 DDS
```

Recommended ROS 2 packages:

```bash
sudo apt update

sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  python3-pip \
  ros-foxy-xacro \
  ros-foxy-robot-state-publisher \
  ros-foxy-joint-state-publisher \
  ros-foxy-joint-state-publisher-gui \
  ros-foxy-rviz2 \
  ros-foxy-ros2-control \
  ros-foxy-ros2-controllers \
  ros-foxy-controller-manager \
  ros-foxy-joint-state-broadcaster \
  ros-foxy-joint-trajectory-controller \
  ros-foxy-control-msgs \
  ros-foxy-trajectory-msgs \
  ros-foxy-moveit
```

Initialize `rosdep` if it has not already been initialized:

```bash
sudo rosdep init 2>/dev/null || true
rosdep update
```

---

## Installation

### 1. Clone the repository as a ROS 2 workspace

This repository already contains a `src/` folder. Therefore, clone it as the workspace root:

```bash
cd ~

git clone https://github.com/jabermahmud24/SO-100-arm-ros2-foxy-Unitree-Go2-ubuntu20.04.git go2_arm_ws
```

Then enter the workspace:

```bash
cd ~/go2_arm_ws
```

The structure should look like:

```bash
ls
```

Expected:

```text
README.md  LICENSE  ACKNOWLEDGMENTS.md  src  scripts
```

Do not clone this repository inside another `src/` folder unless you manually move the internal packages.

---

## Build Instructions

Source ROS 2 Foxy:

```bash
source /opt/ros/foxy/setup.bash
```

Install package dependencies:

```bash
cd ~/go2_arm_ws

rosdep install --from-paths src --ignore-src -r -y
```

Build the workspace:

```bash
colcon build --symlink-install
```

Source the workspace:

```bash
source install/setup.bash
```

Optional: automatically source ROS 2 Foxy and this workspace in every new terminal:

```bash
echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
echo "source ~/go2_arm_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## Build Only the Important Packages

If you want to build only the SO-100 arm-related packages:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash

colcon build --symlink-install --packages-select \
  so_arm_100 \
  so_arm_100_bringup \
  so_arm_100_description \
  so_arm_100_moveit_config \
  so_arm_100_hardware \
  so_arm_100_foxy_bringup
```

Then source:

```bash
source install/setup.bash
```

---

## USB Serial Setup for the Physical Arm

Connect the SO-100 arm USB-to-serial adapter to the Go2 computer.

Check the detected serial device:

```bash
ls /dev/ttyUSB*
```

Usually the device is:

```text
/dev/ttyUSB0
```

Temporary permission fix:

```bash
sudo chmod 666 /dev/ttyUSB0
```

Recommended permanent permission fix:

```bash
sudo usermod -a -G dialout $USER
```

Then log out and log back in, or reboot:

```bash
sudo reboot
```

After reboot:

```bash
groups
```

Make sure `dialout` appears in the group list.

---

## Launch the SO-100 Hardware Interface

Source the workspace:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash
source install/setup.bash
```

Launch the Foxy hardware bringup:

```bash
ros2 launch so_arm_100_foxy_bringup hardware_foxy.launch.py
```

This launch file starts:

- `robot_state_publisher`
- `ros2_control_node`
- `joint_state_broadcaster`
- `arm_controller`

In another terminal, source the workspace again:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash
source install/setup.bash
```

Check controllers:

```bash
ros2 control list_controllers
```

Expected controllers should include something similar to:

```text
joint_state_broadcaster
arm_controller
```

Check hardware interfaces:

```bash
ros2 control list_hardware_interfaces
```

Check joint states:

```bash
ros2 topic echo /joint_states
```

---

## Send a Test Trajectory Command

Make sure the arm is powered, connected, and has enough free space to move.

In a new terminal:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash
source install/setup.bash
```

Send a simple trajectory goal:

```bash
ros2 action send_goal /arm_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: [
      'Shoulder_Rotation',
      'Shoulder_Pitch',
      'Elbow',
      'Wrist_Pitch',
      'Wrist_Roll',
      'Gripper'
    ],
    points: [
      {
        positions: [0.0, -1.0, 1.0, 0.0, 0.0, 0.2],
        velocities: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        time_from_start: {sec: 3, nanosec: 0}
      }
    ]
  }
}"
```

If your controller is configured for only the 5 arm joints without the gripper, use:

```bash
ros2 action send_goal /arm_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: [
      'Shoulder_Rotation',
      'Shoulder_Pitch',
      'Elbow',
      'Wrist_Pitch',
      'Wrist_Roll'
    ],
    points: [
      {
        positions: [0.0, -1.0, 1.0, 0.0, 0.0],
        velocities: [0.0, 0.0, 0.0, 0.0, 0.0],
        time_from_start: {sec: 3, nanosec: 0}
      }
    ]
  }
}"
```

Use the version that matches your controller YAML file.

---

## Run the Example Python Movement Script

This repository includes an example script:

```text
scripts/arm_movement.py
```

Make sure it is executable:

```bash
cd ~/go2_arm_ws
chmod +x scripts/arm_movement.py
```

Run it:

```bash
source /opt/ros/foxy/setup.bash
source install/setup.bash

python3 scripts/arm_movement.py
```

The script sends trajectory goals to:

```text
/arm_controller/follow_joint_trajectory
```

Before running the script, make sure:

```bash
ros2 action list
```

shows:

```text
/arm_controller/follow_joint_trajectory
```

---

## Visualize the Arm in RViz

Source the workspace:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash
source install/setup.bash
```

Launch RViz from the SO-100 package if available:

```bash
ros2 launch so_arm_100 rviz.launch.py
```

Or launch robot state publisher first:

```bash
ros2 launch so_arm_100 rsp.launch.py
```

Then open RViz:

```bash
rviz2
```

In RViz:

1. Set `Fixed Frame` to the robot base frame.
2. Add `RobotModel`.
3. Add `TF`.
4. Add `JointState` if needed.

---

## MoveIt Usage

The repository includes the original MoveIt configuration package:

```text
src/SO-100-arm/so_arm_100_moveit_config/
```

Try launching the MoveIt demo:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash
source install/setup.bash

ros2 launch so_arm_100 demo.launch.py
```

If the launch file is inside the MoveIt config package instead, use:

```bash
ros2 launch so_arm_100_moveit_config demo.launch.py
```

MoveIt support may require additional tuning for the physical Go2-mounted arm, especially for:

- joint limits
- planning frame
- collision geometry
- base-to-arm mounting transform
- gripper configuration
- controller mapping

---

## Unitree Go2 Integration Notes

This repository is intended for the SO-100 arm mounted on the Unitree Go2.

The arm control itself is handled through ROS 2 Control. The Go2 base state can be handled separately through Go2 odometry/state topics.

The optional package:

```text
src/go2_state_bridge/
```

can be used to bridge or republish Go2 state information into cleaner ROS 2 topics for later whole-body integration.

Typical Go2-related topics may include:

```text
/utlidar/robot_odom
/utlidar/robot_pose
/sportmodestate
```

Depending on your Go2 software stack, these can be bridged into cleaner topics such as:

```text
/go2/base_pose
/go2/base_twist
```

This is useful for future whole-body coordination between the Go2 base and the mounted SO-100 arm.

---

## Common Debugging Commands

Check all topics:

```bash
ros2 topic list
```

Check joint states:

```bash
ros2 topic echo /joint_states
```

Check controllers:

```bash
ros2 control list_controllers
```

Check controller manager:

```bash
ros2 node list
ros2 service list | grep controller
```

Check action servers:

```bash
ros2 action list
```

Check whether the arm controller action exists:

```bash
ros2 action info /arm_controller/follow_joint_trajectory
```

Check TF:

```bash
ros2 run tf2_tools view_frames.py
```

Check USB devices:

```bash
lsusb
ls /dev/ttyUSB*
dmesg | grep tty
```

Check serial permission:

```bash
ls -l /dev/ttyUSB0
groups
```

---

## Common Problems and Fixes

### 1. `ros2 launch` cannot find the package

Source the workspace:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash
source install/setup.bash
```

Then check:

```bash
ros2 pkg list | grep so_arm
```

---

### 2. `colcon build` fails because dependencies are missing

Run:

```bash
cd ~/go2_arm_ws
source /opt/ros/foxy/setup.bash

rosdep install --from-paths src --ignore-src -r -y
```

Then rebuild:

```bash
colcon build --symlink-install
```

---

### 3. Permission denied on `/dev/ttyUSB0`

Temporary fix:

```bash
sudo chmod 666 /dev/ttyUSB0
```

Permanent fix:

```bash
sudo usermod -a -G dialout $USER
sudo reboot
```

---

### 4. Controller is not active

Check:

```bash
ros2 control list_controllers
```

If the controller is inactive, try restarting the launch file:

```bash
ros2 launch so_arm_100_foxy_bringup hardware_foxy.launch.py
```

---

### 5. Action server not available

Check:

```bash
ros2 action list
```

If this does not show:

```text
/arm_controller/follow_joint_trajectory
```

then the controller is not running correctly.

Check:

```bash
ros2 control list_controllers
ros2 node list
```

---

### 6. Joint names do not match

Your trajectory command must use the exact joint names expected by the controller.

Common joint names used in this repository are:

```text
Shoulder_Rotation
Shoulder_Pitch
Elbow
Wrist_Pitch
Wrist_Roll
Gripper
```

If the controller YAML uses only 5 joints, remove `Gripper` from the command.

---

## Development Workflow

Whenever you modify files, use:

```bash
cd ~/go2_arm_ws

git status
git add -A
git commit -m "Describe your change"
git pull --rebase origin main
git push origin main
```

Example:

```bash
git add -A
git commit -m "Update Foxy hardware launch file"
git pull --rebase origin main
git push origin main
```

Do not commit generated folders:

```text
build/
install/
log/
```

These folders are generated by `colcon build`.

---

## Recommended `.gitignore`

This repository should ignore ROS 2 build artifacts:

```gitignore
build/
install/
log/

src/build/
src/install/
src/log/

*.pyc
__pycache__/
.vscode/
.DS_Store
```

---

## Safety Notes

Before running the physical arm:

1. Make sure the arm is mechanically secured to the Go2.
2. Make sure the servo power supply is stable.
3. Keep the arm away from the Go2 body, cables, and nearby objects.
4. Start with small joint motions.
5. Keep one hand near the emergency power switch.
6. Do not command large or fast motions until the joint directions and limits are verified.
7. Verify the joint names and signs before running full trajectories.

---



## License

This project preserves the original Apache License 2.0 license from the upstream repositories.

See:

```text
LICENSE
ACKNOWLEDGMENTS.md
```

for license and attribution details.

---



## Disclaimer, No Warranty, and User Responsibility

This repository is provided for research, educational, and experimental robotics use only.

The software, configuration files, launch files, scripts, robot descriptions, and documentation in this repository are provided **"AS IS"**, without warranty of any kind. The author does not guarantee that this repository will work correctly, safely, or reliably on every robot, computer, servo, controller, power system, or ROS 2 installation.

Use of this repository with real hardware is entirely at the user's own risk. Robotic arms, mobile robots, servos, power supplies, batteries, and mounted hardware can cause damage, injury, unexpected motion, electrical failure, mechanical failure, overheating, communication failure, or loss of control if configured or used incorrectly.

By using this repository, the user is solely responsible for:

- verifying all hardware connections;
- checking servo power supply voltage and current limits;
- confirming joint directions, joint limits, and controller parameters;
- testing first in simulation or with motors safely unloaded when possible;
- keeping the robot in a safe, open area during testing;
- using emergency stop or power cutoff procedures;
- complying with all applicable safety rules, lab policies, and local regulations.

The author is not responsible for any damage, injury, data loss, hardware failure, robot malfunction, unsafe motion, or other consequences resulting from the use, modification, or redistribution of this repository.

This repository is not an official Unitree, SO-ARM, Feetech, ROS 2, or manufacturer-supported product. Use it only if you understand the risks of operating experimental robotic hardware.

See the `LICENSE` file for the full Apache License 2.0 terms, including disclaimer of warranty and limitation of liability.

---

## Citation / Reference

If you use this repository, please cite or acknowledge both this adaptation and the original upstream repositories:

```text
Original SO-100 ROS 2 repository:
https://github.com/brukg/SO-100-arm

Original SO-100 hardware interface:
https://github.com/brukg/so_arm_100_hardware

ROS 2 Foxy / Unitree Go2 adaptation:
https://github.com/jabermahmud24/SO-100-arm-ros2-foxy-Unitree-Go2-ubuntu20.04
```