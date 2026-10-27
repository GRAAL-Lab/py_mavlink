# py_mavlink

A ROS 2 package for receiving MAVLink telemetry from a UAV or MAVLink-enabled device and publishing the decoded data as ROS messages on topics.

This package is intended to bridge MAVLink data into ROS-based applications, making it easier to consume vehicle state, sensor, and other telemetry data in a ROS 2 ecosystem.

## Overview

`py_mavlink` connects to a MAVLink stream, listens for incoming messages, converts relevant fields into custom ROS message types and standard ROS message types, and publishes them on ROS topics.

The package currently includes:
- a MAVLink publisher node that listens for telemetry such as attitude, battery status, RC input/output, and IMU/pressure values
- a camera image node that requests/receives camera-related MAVLink messages and republishes the image stream as a ROS `sensor_msgs/Image`

This package is designed to work alongside the `mavlink_msg` package, which defines the custom ROS message interfaces used for published telemetry.

## Features

- Connect to MAVLink-enabled UAVs or autopilots over UDP
- Decode common MAVLink messages
- Convert MAVLink fields into ROS message types
- Publish telemetry to ROS topics
- Publish camera image data as ROS `Image` messages
- Integrate cleanly into ROS 2 systems

## Package Contents

- `py_mavlink/publisher_mavlink_msg.py`
  - Main MAVLink data publishing node
- `py_mavlink/camera_image_node.py`
  - Node for camera image capture and publication
- `package.xml`
  - ROS package metadata and dependencies
- `setup.py`
  - Python package configuration and entry points

## Dependencies

This package depends on the following:

- ROS 2
- `rclpy`
- `std_msgs`
- `sensor_msgs`
- `pymavlink`
- `mavros`
- `mavros_msgs`
- `mavlink_msg` (custom ROS message package)

The `mavlink_msg` package is required because it defines the custom message interfaces used for telemetry publishing.

## Installation

From a ROS 2 workspace:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

git clone https://github.com/GRAAL-Lab/mavlink_msg.git
git clone https://github.com/GRAAL-Lab/py_mavlink.git

cd ~/ros2_ws
colcon build --packages-select py_mavlink
source install/setup.bash
```

If you are using a different ROS 2 distribution, make sure the required packages are installed and the workspace is sourced appropriately.

## Running the Nodes

### 1. MAVLink Telemetry Publisher

```bash
ros2 run py_mavlink mavlink_publisher
```

This node listens for MAVLink messages and publishes them to topics such as:

- `/bluerov2/attitude`
- `/bluerov2/battery_status`
- `/bluerov2/rc_channels`
- `/bluerov2/servo_output`
- `/bluerov2/raw_imu`
- `/bluerov2/scaled_imu2`
- `/bluerov2/scaled_pressure`
- `/bluerov2/scaled_pressure2`

### 2. Camera Image Publisher

```bash
ros2 run py_mavlink camera_publisher
```

This node establishes a MAVLink connection and attempts to request and publish camera image data on:

- `/camera/image`

## Published Data

The MAVLink publisher currently converts and publishes the following message types:

- `ATTITUDE`
- `BATTERY_STATUS`
- `RC_CHANNELS`
- `SERVO_OUTPUT_RAW`
- `RAW_IMU`
- `SCALED_IMU2`
- `SCALED_PRESSURE`
- `SCALED_PRESSURE2`

These values are converted into ROS messages and published with timestamps from the ROS system clock.

## Connection Configuration

The publisher currently listens on:

```python
udpin:0.0.0.0:14551
```

This means it expects incoming MAVLink traffic on UDP port `14551` by default.

The camera node uses:

```python
udp:192.168.2.1:14770
```

This is an example connection string and may need to be adjusted to match your MAVLink device or network configuration.

## Notes

- The camera stream implementation depends heavily on the target UAV and its MAVLink camera/image capabilities.
- The exact camera command and message handling may require adjustments for different drone models or firmware versions.
- You may need to modify connection strings, topic names, or message handling logic to match your hardware setup.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.

## Contributing

Contributions are welcome. If you want to improve message conversion, add support for more MAVLink messages, or improve reliability for camera streaming, feel free to open a pull request or submit an issue.

## Authors

This package is maintained by the GRAAL Lab project team.

## Contact

For questions or support, please refer to the repository owner or project maintainers associated with the GRAAL Lab organization.
