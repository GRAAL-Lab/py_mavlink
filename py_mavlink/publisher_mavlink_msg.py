import rclpy
from rclpy.node import Node
from pymavlink import mavutil
from mavlink_msg.msg import BatteryStatus
from mavros_msgs.msg import RCIn
from mavros_msgs.msg import RCOut
from mavlink_msg.msg import IMU
from mavlink_msg.msg import Pressure
from mavlink_msg.msg import Attitude

from std_msgs.msg import String


class MavlinkMsgPublisher(Node):
    def __init__(self):
        super().__init__('mavlink_msg_publisher')

        # MAVLink Connection
        # Start a connection listening to a UDP port
        #self.connection = mavutil.mavlink_connection('udpin:192.168.2.1:14770')
        #self.connection = mavutil.mavlink_connection('udpin:192.168.2.1:14771')
        ##self.connection = mavutil.mavlink_connection('udpin:192.168.2.255:14551')
        self.connection = mavutil.mavlink_connection('udpin:0.0.0.0:14551')
        self.get_logger().info("Waiting for a heartbeat...")
        self.connection.wait_heartbeat()
        self.get_logger().info("Heartbeat received!")

        # Publisher
        self.attitude_publisher = self.create_publisher(Attitude, '/bluerov2/attitude', 20)
        self.battery_status_publisher = self.create_publisher(BatteryStatus, '/bluerov2/battery_status', 20)
        self.rc_channels_publisher = self.create_publisher(RCIn, '/bluerov2/rc_channels', 20)
        self.sevo_output_publisher = self.create_publisher(RCOut, '/bluerov2/servo_output', 20)
        self.raw_imu_publisher = self.create_publisher(IMU, '/bluerov2/raw_imu', 20)
        self.scaled_imu2_publisher = self.create_publisher(IMU, '/bluerov2/scaled_imu2', 20)
        self.scaled_pressure_publisher = self.create_publisher(Pressure, '/bluerov2/scaled_pressure', 20)
        self.scaled_pressure2_publisher = self.create_publisher(Pressure, '/bluerov2/scaled_pressure2', 20)

        # Timers for data and control loops
        timer_period = 0.01
        self.data_timer = self.create_timer(timer_period, self.receive_data)  # 100 Hz
        """Continuously receive data from MAVLink."""
        self.get_logger().info("Continuously receive data from MAVLink.")
        self.get_logger().info("'ATTITUDE', 'BATTERY_STATUS', 'RC_CHANNELS', 'SERVO_OUTPUT_RAW'")
        #self.control_loop_timer = self.create_timer(0.1, self.control_loop)  # 10 Hz

        


    def receive_data(self):        
        msg = self.connection.recv_match(type=['ATTITUDE', 'BATTERY_STATUS', 'RC_CHANNELS', 'SERVO_OUTPUT_RAW',
                                                'RAW_IMU', 'SCALED_IMU2', 'SCALED_PRESSURE','SCALED_PRESSURE2'], blocking=False)

        if msg:
            if msg.get_type() == 'ATTITUDE':
                attitude_msg = Attitude()
                attitude_msg.time_boot_ms = msg.time_boot_ms
                attitude_msg.header.stamp = self.get_clock().now().to_msg()
                attitude_msg.roll = msg.roll # rad
                attitude_msg.pitch = msg.pitch # rad
                attitude_msg.yaw = msg.yaw # rad
                attitude_msg.roll_speed = msg.rollspeed # rad/s
                attitude_msg.pitch_speed = msg.pitchspeed # rad/s
                attitude_msg.yaw_speed = msg.yawspeed # rad/s
                self.attitude_publisher.publish(attitude_msg)
                #print(msg)
            
            elif msg.get_type() == 'BATTERY_STATUS':
                battery_msg = BatteryStatus()
                battery_msg.header.stamp = self.get_clock().now().to_msg()
                for i in range(0, 10):
                    battery_msg.voltages[i] = msg.voltages[i]
                battery_msg.current_battery = msg.current_battery # real time curent measurment
                battery_msg.current_consumed = msg.current_consumed # consumed current
                battery_msg.energy_consumed = msg.energy_consumed # consumed energy
                battery_msg.battery_remaining = msg.battery_remaining
                battery_msg.time_remaining = msg.time_remaining
                battery_msg.charge_state = msg.charge_state
                battery_msg.temperature = msg.temperature
                self.battery_status_publisher.publish(battery_msg)
                
            elif msg.get_type() == 'RC_CHANNELS':
                rc_msg = RCIn()
                rc_msg.header.stamp = self.get_clock().now().to_msg()
                rc_msg.channels.append(msg.chan1_raw)
                rc_msg.channels.append(msg.chan2_raw)
                rc_msg.channels.append(msg.chan3_raw)
                rc_msg.channels.append(msg.chan4_raw)
                rc_msg.channels.append(msg.chan5_raw)
                rc_msg.channels.append(msg.chan6_raw)
                rc_msg.channels.append(msg.chan7_raw)
                rc_msg.channels.append(msg.chan8_raw)
                rc_msg.channels.append(msg.chan9_raw)
                rc_msg.channels.append(msg.chan10_raw)
                rc_msg.channels.append(msg.chan11_raw)
                rc_msg.channels.append(msg.chan12_raw)
                rc_msg.channels.append(msg.chan13_raw)
                rc_msg.channels.append(msg.chan14_raw)
                rc_msg.channels.append(msg.chan15_raw)
                rc_msg.channels.append(msg.chan16_raw)
                rc_msg.channels.append(msg.chan17_raw)
                rc_msg.channels.append(msg.chan18_raw)
                rc_msg.rssi = msg.rssi
                self.rc_channels_publisher.publish(rc_msg)
                #print(msg)

            elif msg.get_type() == 'SERVO_OUTPUT_RAW':
                rc_msg = RCOut()
                rc_msg.header.stamp = self.get_clock().now().to_msg()
                rc_msg.channels.append(msg.servo1_raw)
                rc_msg.channels.append(msg.servo2_raw)
                rc_msg.channels.append(msg.servo3_raw)
                rc_msg.channels.append(msg.servo4_raw)
                rc_msg.channels.append(msg.servo5_raw)
                rc_msg.channels.append(msg.servo6_raw)
                rc_msg.channels.append(msg.servo7_raw)
                rc_msg.channels.append(msg.servo8_raw)
                rc_msg.channels.append(msg.servo9_raw)
                rc_msg.channels.append(msg.servo10_raw)
                rc_msg.channels.append(msg.servo11_raw)
                rc_msg.channels.append(msg.servo12_raw)
                rc_msg.channels.append(msg.servo13_raw)
                rc_msg.channels.append(msg.servo14_raw)
                rc_msg.channels.append(msg.servo15_raw)
                rc_msg.channels.append(msg.servo16_raw)
                self.sevo_output_publisher.publish(rc_msg)
                #print(msg)

            elif msg.get_type() == 'RAW_IMU':
                imu_msg = IMU()
                imu_msg.header.stamp = self.get_clock().now().to_msg()
                imu_msg.time_usec = msg.time_usec # us
                imu_msg.xacc = msg.xacc # mG
                imu_msg.yacc = msg.yacc # mG
                imu_msg.zacc = msg.zacc # mG
                imu_msg.xgyro = msg.xgyro # mrad/s
                imu_msg.ygyro = msg.ygyro # mrad/s
                imu_msg.zgyro = msg.zgyro # mrad/s
                imu_msg.xmag = msg.xmag # mgauss
                imu_msg.ymag = msg.ymag # mgauss
                imu_msg.zmag = msg.zmag # mgauss
                imu_msg.id = msg.id 
                imu_msg.temperature = msg.temperature # cdegC
                self.raw_imu_publisher.publish(imu_msg)

            elif msg.get_type() == 'SCALED_IMU2':
                imu_msg = IMU()
                imu_msg.header.stamp = self.get_clock().now().to_msg()
                imu_msg.time_usec = msg.time_boot_ms # ms
                imu_msg.xacc = msg.xacc # mG
                imu_msg.yacc = msg.yacc # mG
                imu_msg.zacc = msg.zacc # mG
                imu_msg.xgyro = msg.xgyro # mrad/s
                imu_msg.ygyro = msg.ygyro # mrad/s
                imu_msg.zgyro = msg.zgyro # mrad/s
                imu_msg.xmag = msg.xmag # mgauss
                imu_msg.ymag = msg.ymag # mgauss
                imu_msg.zmag = msg.zmag # mgauss
                imu_msg.temperature = msg.temperature # cdegC
                self.scaled_imu2_publisher.publish(imu_msg)

            elif msg.get_type() == 'SCALED_PRESSURE':
                pressure_msg = Pressure()
                pressure_msg.header.stamp = self.get_clock().now().to_msg()
                pressure_msg.time_boot_ms = msg.time_boot_ms # ms
                pressure_msg.press_abs = msg.press_abs # Absolute pressure (hPa)
                pressure_msg.press_diff = msg.press_diff # Differential pressure
                pressure_msg.temperature = msg.temperature # Absolute pressure temperature (cdegC)
                pressure_msg.temperature_press_diff = msg.temperature_press_diff # Differential pressure temperature (0, if not available) (cdegC)
                self.scaled_pressure_publisher.publish(pressure_msg)

            elif msg.get_type() == 'SCALED_PRESSURE2':
                pressure_msg = Pressure()
                pressure_msg.header.stamp = self.get_clock().now().to_msg()
                pressure_msg.time_boot_ms = msg.time_boot_ms # ms
                pressure_msg.press_abs = msg.press_abs# Absolute pressure (hPa)
                pressure_msg.press_diff = msg.press_diff # Differential pressure
                pressure_msg.temperature = msg.temperature # Absolute pressure temperature (cdegC)
                pressure_msg.temperature_press_diff = msg.temperature_press_diff # Differential pressure temperature (0, if not available) (cdegC)
                self.scaled_pressure2_publisher.publish(pressure_msg)
                



def main(args=None):
    rclpy.init(args=args)
    mavlink_msg_publisher = MavlinkMsgPublisher()
    rclpy.spin(mavlink_msg_publisher)
    mavlink_msg_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
