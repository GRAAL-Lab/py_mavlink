1| # py_mavlink
2| 
3| A ROS 2 package for receiving MAVLink telemetry from a UAV or MAVLink-enabled device and publishing the decoded data as ROS messages on topics.
4| 
5| This package is intended to bridge MAVLink data into ROS-based applications, making it easier to consume vehicle state, sensor, and other telemetry data in a ROS 2 ecosystem.
6| 
7| ## Overview
8| 
9| `py_mavlink` connects to a MAVLink stream, listens for incoming messages, converts relevant fields into custom ROS message types and standard ROS message types, and publishes them on ROS topics.
10| 
11| The package currently includes:
12| - a MAVLink publisher node that listens for telemetry such as attitude, battery status, RC input/output, and IMU/pressure values
13| - a camera image node that requests/receives camera-related MAVLink messages and republishes the image stream as a ROS `sensor_msgs/Image`
14| 
15| This package is designed to work alongside the `mavlink_msg` package, which defines the custom ROS message interfaces used for published telemetry.
16| 
17| ## Features
18| 
19| - Connect to MAVLink-enabled UAVs or autopilots over UDP
20| - Decode common MAVLink messages
21| - Convert MAVLink fields into ROS message types
22| - Publish telemetry to ROS topics
23| - Publish camera image data as ROS `Image` messages
24| - Integrate cleanly into ROS 2 systems
25| 
26| ## Package Contents
27| 
28| - `py_mavlink/publisher_mavlink_msg.py`
29|   - Main MAVLink data publishing node
30| - `py_mavlink/camera_image_node.py`
31|   - Node for camera image capture and publication
32| - `package.xml`
33|   - ROS package metadata and dependencies
34| - `setup.py`
35|   - Python package configuration and entry points
36| 
37| ## Dependencies
38| 
39| This package depends on the following:
40| 
41| - ROS 2
42| - `rclpy`
43| - `std_msgs`
44| - `sensor_msgs`
|45| - `pymavlink`
46| - `mavros`
47| - `mavros_msgs`
48| - `mavlink_msg` (custom ROS message package)
49| 
50| The `mavlink_msg` package is required because it defines the custom message interfaces used for telemetry publishing.
51| 
52| ## Installation
53| 
54| From a ROS 2 workspace:
55| 
|56| ```bash
57| mkdir -p ~/ros2_ws/src
58| cd ~/ros2_ws/src
59| 
60| git clone https://github.com/GRAAL-Lab/mavlink_msg.git
61| git clone https://github.com/GRAAL-Lab/py_mavlink.git
62| 
63| cd ~/ros2_ws
64| colcon build --packages-select py_mavlink
65| source install/setup.bash
66| ```
67| 
68| ### Install required dependencies before running the node
69| 
70| Install the Python MAVLink library and MAVROS before launching the ROS nodes:
71| 
72| ```bash
73| sudo apt update
74| sudo apt install -y python3-pip python3-rosdep
75| 
76| pip3 install pymavlink
77| sudo apt install -y ros-$(ros2 pkg list >/dev/null 2>&1; echo $ROS_DISTRO)-mavros
78| ```
79| 
80| If you are using a different ROS 2 distribution, make sure the required packages are installed and the workspace is sourced appropriately.
81| 
82| ## Running the Nodes
83| 
84| ### 1. MAVLink Telemetry Publisher
85| 
86| ```bash
87| ros2 run py_mavlink mavlink_publisher
88| ```
89| 
90| This node listens for MAVLink messages and publishes them to topics such as:
91| 
92| - `/bluerov2/attitude`
93| - `/bluerov2/battery_status`
94| - `/bluerov2/rc_channels`
|94| - `/bluerov2/servo_output`
95| - `/bluerov2/raw_imu`
96| - `/bluerov2/scaled_imu2`
97| - `/bluerov2/scaled_pressure`
98| - `/bluerov2/scaled_pressure2`
99| 
100| ### 2. Camera Image Publisher
101| 
102| ```bash
103| ros2 run py_mavlink camera_publisher
104| ```
105| 
106| This node establishes a MAVLink connection and attempts to request and publish camera image data on:
107| 
108| - `/camera/image`
109| 
110| ## Published Data
111| 
112| The MAVLink publisher currently converts and publishes the following message types:
113| 
114| - `ATTITUDE`
115| - `BATTERY_STATUS`
116| - `RC_CHANNELS`
117| - `SERVO_OUTPUT_RAW`
118| - `RAW_IMU`
119| - `SCALED_IMU2`
120| - `SCALED_PRESSURE`
121| - `SCALED_PRESSURE2`
122| 
123| These values are converted into ROS messages and published with timestamps from the ROS system clock.
124| 
125| ## Connection Configuration
126| 
127| The publisher currently listens on:
128| 
129| ```python
130| udpin:0.0.0.0:14551
131| ```
132| 
133| This means it expects incoming MAVLink traffic on UDP port `14551` by default.
134| 
135| The camera node uses:
136| 
137| ```python
138| udp:192.168.2.1:14770
139| ```
140| 
141| This is an example connection string and may need to be adjusted to match your MAVLink device or network configuration.
142| 
143| ## Notes
144| 
145| - The camera stream implementation depends heavily on the target UAV and its MAVLink camera/image capabilities.
146| - The exact camera command and message handling may require adjustments for different drone models or firmware versions.
147| - You may need to modify connection strings, topic names, or message handling logic to match your hardware setup.
148| 
149| ## License
150| 
151| This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
152| 
153| ## Contributing
154| 
155| Contributions are welcome. If you want to improve message conversion, add support for more MAVLink messages, or improve reliability for camera streaming, feel free to open a pull request or submit an issue.
156| 
157| ## Authors
158| 
159| This package is maintained by the GRAAL Lab project team.
160| 
161| ## Contact
162| 
163| For questions or support, please refer to the repository owner or project maintainers associated with the GRAAL Lab organization.
164| 