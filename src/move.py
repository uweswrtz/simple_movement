#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist


def move():
    # Starts a new node
    rospy.init_node('simple_move_move', anonymous=True)
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    rate = rospy.Rate(10) # 10hz

    #Receiveing the user's input
    print("Let's move your robot")
    speed = input("Input your speed:")
    distance = input("Type your distance:")
    isForward = input("Forward?: ")#True or False
    isReturn = input("Return?:")#True or False
    isEndless= input("Endless?:")#True or False

    #Checking if the movement is forward or backwards
    if(isForward):
        #vel_msg.linear.x = abs(speed)
        speed = abs(speed)
    else:
        #vel_msg.linear.x = -abs(speed)
        speed = -abs(speed)

    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while not rospy.is_shutdown():
        
        vel_msg.linear.x = speed

        #Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        rospy.loginfo(rospy.get_caller_id() + " publish velocity %s", vel_msg.linear.x)
        #Loop to move the turtle in an specified distance
        while(current_distance < distance):
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
            current_distance= abs(speed)*(t1-t0)
            rate.sleep()
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        rospy.loginfo(rospy.get_caller_id() + " publish velocity %s", vel_msg.linear.x)
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)


        #Return robot
        if(isReturn):
            rospy.sleep(1)
            vel_msg.linear.x = -1 * speed
            t0 = rospy.Time.now().to_sec()
            current_distance = 0

            rospy.loginfo(rospy.get_caller_id() + " publish velocity %s", vel_msg.linear.x)
            #Loop to move the turtle in an specified distance
            while(current_distance < distance):
                #Publish the velocity
                velocity_publisher.publish(vel_msg)
                #Takes actual time to velocity calculus
                t1=rospy.Time.now().to_sec()
                #Calculates distancePoseStamped
                current_distance= abs(speed)*(t1-t0)
                rate.sleep()
            #After the loop, stops the robot
            vel_msg.linear.x = 0
            rospy.loginfo(rospy.get_caller_id() + " publish velocity %s", vel_msg.linear.x)
            #Force the robot to stop
            velocity_publisher.publish(vel_msg)

        if not isEndless or not isReturn:
            exit()

        rospy.sleep(1)

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass
