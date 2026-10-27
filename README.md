# py_mavlink

ROS package to convert MAVLink messages to ROS messages and publish them on ROS topics.

## Overview

`py_mavlink` is a ROS package designed to receive MAVLink telemetry, convert it into ROS-native message types, and publish the converted data on ROS topics for use in ROS 2 applications.

This package is intended to work together with the `mavlink_msg` package, which defines the custom ROS message interfaces used for the published data. The resulting ROS topics can then be consumed by downstream nodes for logging, visualization, control, monitoring, and processing.

## Features

- Decode MAVLink messages from UAV or MAVLink-enabled systems
- Convert MAVLink data into ROS messages
- Publish converted values on ROS topics
- Integrate with ROS 2 nodes and tools
- Work with custom message definitions provided by `mavlink_msg`

## Dependencies

This package depends on:

- `rclpy`
- `std_msgs`
- `sensor_msgs`
- `pymavlink`
- `mavlink_msg`

The `mavlink_msg` package is a required dependency and provides the message definitions used for publishing MAVLink-derived telemetry on ROS topics.

## Build

From a ROS 2 workspace:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/GRAAL-Lab/mavlink_msg.git
git clone https://github.com/GRAAL-Lab/py_mavlink.git
cd ~/ros2_ws
colcon build --packages-select py_mavlink
source install/setup.bash
