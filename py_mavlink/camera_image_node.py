import rclpy
from rclpy.node import Node
from pymavlink import mavutil
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraImageNode(Node):
    def __init__(self):
        super().__init__('camera_image_node')
        
        # Initialize MAVLink connection to the drone
        self.mavlink_connection = mavutil.mavlink_connection('udp:192.168.2.1:14770')  # Change to your connection string
        self.mavlink_connection.wait_heartbeat()
        self.get_logger().info("MAVLink connection established!")

        # Set up the ROS 2 publisher to publish camera images
        self.image_publisher = self.create_publisher(Image, 'camera/image', 10)
        self.bridge = CvBridge()

        # Request camera status or start stream (depends on your setup)
        self.request_camera_stream()

    def request_camera_stream(self):
        # Send MAVLink message to start video stream (change depending on your UAV's capabilities)
        self.mavlink_connection.mav.command_long_send(
            1,  # Target system ID (usually 1 for most drones)
            1,  # Target component ID (usually 1 for the autopilot)
            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,  # Request a specific MAVLink message
            0,  # Confirmation (usually 0)
            mavutil.mavlink.MAVLINK_MSG_ID_CAMERA_IMAGE_CAPTURED,  # Message ID
            0, 0, 0, 0, 0, 0  # Parameters for your message
        )
        self.get_logger().info("Requested camera stream.")

    def process_mavlink_messages(self):
        while rclpy.ok():
            self.get_logger().info("spinning.")
            message = self.mavlink_connection.recv_match(type='CAMERA_IMAGE_CAPTURED', blocking=False)
            self.get_logger().info("match recieved.")
            if message:
                self.get_logger().info("Message received.")
                # Process image capture message and retrieve image data
                # You can also use MAV_CMD_VIDEO_STREAM to start streaming
                self.get_logger().info(f"Received camera image capture message: {message}")
                self.publish_camera_image(message)
            else:
                self.get_logger().info("No message received.")

    def publish_camera_image(self, message):
        # Example: Convert message data to OpenCV format and publish it as a ROS Image message
        # (This depends on your drone's implementation and image format)
        # For example, if you have raw image data, you can process and publish it
        image_data = message.image_data  # This would be in a specific format, depending on your drone
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        if image is not None:
            ros_image = self.bridge.cv2_to_imgmsg(image, encoding='bgr8')
            self.image_publisher.publish(ros_image)
            self.get_logger().info("Published camera image.")

def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraImageNode()
    print('camera node initiated')
    # Process MAVLink messages and send images
    camera_node.process_mavlink_messages()

    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

