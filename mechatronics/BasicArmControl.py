import traceback

from Phidget22.Devices.Log import *
from Phidget22.Devices.Stepper import *
from Phidget22.LogLevel import *
from Phidget22.Phidget import *
from pyPS4Controller.controller import Controller


class MyController(Controller):
    global base_motor, shoulder_motor1, shoulder_motor2, elbow_motor, wrist_motor, claw_motor

    # Base motor movement keys
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_L2_press(self, value):
        if not base_motor.getIsMoving():
            base_motor.setVelocityLimit(30)

    def on_L2_release(self):
        base_motor.setVelocityLimit(0)

    def on_R2_press(self, value):
        if not base_motor.getIsMoving():
            base_motor.setVelocityLimit(-30)

    def on_R2_release(self):
        base_motor.setVelocityLimit(0)

    # Shoulder motor movement keys
    def on_L3_up(self, value):
        if not shoulder_motor1.getIsMoving():
            shoulder_motor1.setVelocityLimit(50)
            shoulder_motor2.setVelocityLimit(-50)

    def on_L3_down(self, value):
        if not shoulder_motor1.getIsMoving():
            shoulder_motor1.setVelocityLimit(-50)
            shoulder_motor2.setVelocityLimit(50)

    # Elbow motor movement keys
    def on_R3_up(self, value):
        if not elbow_motor.getIsMoving():
            elbow_motor.setVelocityLimit(50)

    def on_R3_down(self, value):
        if not elbow_motor.getIsMoving():
            elbow_motor.setVelocityLimit(-50)

    # Wrist motor movement keys
    def on_L1_press(self):
        if not wrist_motor.getIsMoving():
            wrist_motor.setVelocityLimit(50)

    def on_L1_release(self):
        wrist_motor.setVelocityLimit(0)

    def on_R1_press(self):
        if not wrist_motor.getIsMoving():
            wrist_motor.setVelocityLimit(-50)

    def on_R1_release(self):
        wrist_motor.setVelocityLimit(0)

    # Claw motor movement keys
    def on_x_press(self):
        if not claw_motor.getIsMoving():
            claw_motor.setVelocityLimit(20)

    def on_x_release(self):
        claw_motor.setVelocityLimit(0)

    def on_triangle_press(self):
        if not claw_motor.getIsMoving():
            claw_motor.setVelocityLimit(-20)

    def on_triangle_release(self):
        wrist_motor.setVelocityLimit(0)

    # hold position
    def on_circle_press(self):
        claw_motor.setVelocityLimit(0)

    def on_playstation_button_press(self):
        print("Quitting programming...")
        base_motor.setEngaged(False)
        shoulder_motor1.setEngaged(False)
        shoulder_motor2.setEngaged(False)
        elbow_motor.setEngaged(False)
        wrist_motor.setEngaged(False)
        claw_motor.setEngaged(False)
        return False

    def on_options_press(self):
        base_motor.setTargetPosition((base_motor.getMaxPosition() + base_motor.getMinPosition()) / 2)
        shoulder_motor1.setTargetPosition((shoulder_motor1.getMaxPosition() + shoulder_motor1.getMinPosition()) / 2)
        shoulder_motor2.setTargetPosition((shoulder_motor2.getMaxPosition() + shoulder_motor2.getMinPosition()) / 2)
        wrist_motor.setTargetPosition((wrist_motor.getMaxPosition() + wrist_motor.getMinPosition()) / 2)
        elbow_motor.setTargetPosition((elbow_motor.getMaxPosition() + elbow_motor.getMinPosition()) / 2)
        claw_motor.setTargetPosition((claw_motor.getMaxPosition() + claw_motor.getMinPosition()) / 2)


def onAttach(motor_number):
    print("Motor {0} attached!".format(motor_number))


def onDetach(self):
    print("Detach!")
    # print("Motor {0} detached!".format(motor_number))


def onError(self, code, description):
    print("Code: " + ErrorEventCode.getName(code))
    print("Description: " + str(description))
    print("----------")


def initialize_motors(motors, motors_info):
    for i in range(len(motors)):
        motors[i].setDeviceSerialNumber(620000)
        motors[i].setHubPort(i)
        motors[i].setOnAttachHandler(onAttach(i))
        motors[i].setOnDetachHandler(onDetach)
        motors[i].setOnErrorHandler(onError)
        motors[i].openWaitForAttachment(5000)
        motors[i].setControlMode(StepperControlMode.CONTROL_MODE_RUN)
        motors[i].setCurrentLimit(motors_info[i][0])
        motors[i].setHoldingCurrentLimit(motors_info[i][1])
        motors[i].setRescaleFactor(1.8 / 16 / motors_info[i][2])
        motors[i].setAcceleration(50)
        motors[i].setVelocityLimit(0)
        motors[i].setEngaged(True)
        motors[i].setDataInterval(motors[i].getMinDataInterval())


# -----------------------------------------------------  MAIN  --------------------------------------------------------
# Declare and initialize motors and motor info (current limit, holding current, gear ratio)
base_motor = Stepper()  # Rotates base
base_motor_info = [2.8, 1, 77]
shoulder_motor1 = Stepper()  # Reference motor to rotate shoulder joint
shoulder_motor1_info = [2.8, 2.8, 15]
shoulder_motor2 = Stepper()  # Support motor to rotate shoulder joint (inverse of shoulder_motor1)
shoulder_motor2_info = [2.8, 0, 15]
elbow_motor = Stepper()  # Rotates elbow
elbow_motor_info = [2.8, 1, 15]
wrist_motor = Stepper()  # Rotates wrist
wrist_motor_info = [0.67, 0.67, 100]
claw_motor = Stepper()  # Pinches claw
claw_motor_info = [0.67, 0, 100]

all_motor_names = [base_motor, shoulder_motor1, shoulder_motor2, elbow_motor, wrist_motor, claw_motor]
all_motor_info = [base_motor_info, shoulder_motor1_info, shoulder_motor2_info, elbow_motor_info, wrist_motor_info,
                  claw_motor_info]

try:
    Log.enable(LogLevel.PHIDGET_LOG_INFO, "PhidgetArmLog.log")
    initialize_motors(all_motor_names, all_motor_info)

    # Collect events until released
    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()

    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    # you can start listening before controller is paired, as long as you pair it within the timeout window
    controller.listen(timeout=60)
    # try:
    #    input("Press Enter to Stop\n")
    # except (Exception, KeyboardInterrupt):
    #    pass

    base_motor.close()
    shoulder_motor1.close()
    shoulder_motor2.close()
    elbow_motor.close()
    wrist_motor.close()
    claw_motor.close()

except PhidgetException as ex:
    # We will catch Phidget Exceptions here, and print the error information.
    traceback.print_exc()
    print("")
    print("PhidgetException " + str(ex.code) + " (" + ex.description + "): " + ex.details)

print("DONE")
