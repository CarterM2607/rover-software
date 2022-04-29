#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix

from Phidget22.Phidget import *
from Phidget22.Devices.LCD import *
import time

def callback(data, args):
    coords = str(round(data.latitude, 6)) + ", " + str(round(data.longitude, 6))
    args.writeText(LCDFont.FONT_5x8, 0, 0, "GPS Coords:")
    args.writeText(LCDFont.FONT_5x8, 0, 10, coords)
    args.flush()

def main():
    rospy.init_node('lcd_display', anonymous=True)

    lcd0 = LCD()

    lcd0.openWaitForAttachment(5000)

    lcd0.setBacklight(0.5)

    rospy.Subscriber("gps_ublox/fix", NavSatFix, callback, (lcd0))

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass