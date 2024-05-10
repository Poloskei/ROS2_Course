import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
#import turtle_proportionate_controller as tpc

class TurtlesimController(Node):

    def __init__(self):
        super().__init__('turtlesim_controller')

        self.declare_parameter('speed', 8.0)
        self.declare_parameter('omega', 175.0)

        self.pose = None
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.cb_pose,
            10)

        self.twist_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def cb_pose(self, msg):
        self.pose = msg


    def go_straight(self, distance):
        while self.pose is None and rclpy.ok():
            self.get_logger().info('Waiting for pose??...')
            rclpy.spin_once(self)

        x0 = self.pose.x
        y0 = self.pose.y
        vel_msg=Twist()
        distance_curr = math.sqrt(((self.pose.x- x0) * (self.pose.x - x0)) + ((self.pose.y - y0) * (self.pose.y - y0)))

        while (distance_curr < distance) and rclpy.ok():
            diff = distance-distance_curr
            if  diff > distance*0.1:
                vel_msg.linear.x = (diff*3)

            self.twist_pub.publish(vel_msg)
            rclpy.spin_once(self)
            #self.get_logger().info('On its way...')
            delta_x = self.pose.x - x0
            delta_y = self.pose.y - y0
            distance_curr = (delta_x**2 + delta_y**2)**0.5


        # Set velocity to 0
        delta_x = x0-self.pose.x
        delta_y = y0-self.pose.y
        distance_curr = (delta_x**2 + delta_y**2)**0.5
        #print(distance_curr, " vs ",distance)
        vel_msg.linear.x = 0.0
        self.twist_pub.publish(vel_msg)
        #self.get_logger().info('Arrived to destination.')


    def turn(self, angle):
        while self.pose is None and rclpy.ok():
            self.get_logger().info('Waiting for pose??...')
            rclpy.spin_once(self)
        omega = self.get_parameter('omega').get_parameter_value().double_value
        theta0 = self.pose.theta
        vel_msg = Twist()

        # Publish first msg and note time
        #self.get_logger().info('Turtle started.')


        target = theta0 +math.radians(angle)
        diff = math.radians(angle)
        while diff > math.pi:
            diff -= 2.0 * math.pi
        while diff < -math.pi:

            diff += 2.0 * math.pi



        while abs(diff) > 0.0002:
            #if abs(diff) > 0.00001:
            vel_msg.angular.z = diff * 2
            self.twist_pub.publish(vel_msg)
            rclpy.spin_once(self)
            diff = target - self.pose.theta
            while diff > math.pi:
                diff -= 2.0 * math.pi
            while diff < -math.pi:
                print("added pi ", diff)
                diff += 2.0 * math.pi
            print(diff)


        # Publish msg while the calculated time is up




        # Set velocity to 0
        vel_msg.angular.z = 0.0
        self.twist_pub.publish(vel_msg)
        #self.get_logger().info('Arrived to destination.')


    def fractal(self,len,depth):
        for i in range(3):
            self.fractal_rec(len,depth)
            self.turn(120)


    def fractal_rec(self, len, depth):
        if depth == 0:
            self.go_straight(len)
        else:
            self.fractal_rec(len/3,depth-1)
            self.turn(-60)
            self.fractal_rec(len/3,depth-1)
            self.turn(120)
            self.fractal_rec(len/3,depth-1)
            self.turn(-60)
            self.fractal_rec(len/3,depth-1)



def main(args=None):
    rclpy.init(args=args)
    tc = TurtlesimController()
    #tc.turn(20.0,90.0)
    #tc.go_straight(1.0,4.0)

    #tc.draw_poly(10,2.3)
    tc.fractal(4.5,3)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tc.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
