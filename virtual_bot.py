from sr.robot import *
from typing import Union, Tuple


def signum(x):
    if x < 0:
        return - 1
    return 1


class VirtualBot(Robot):
    @property
    def left_motor(self):
        return self.motors[0].m0

    @property
    def right_motor(self):
        return self.motors[0].m1

    @property
    def lift_motor(self):
        return self.motors[1].m0

    @property
    def gripper_motor(self):
        return self.motors[1].m1

    @property
    def front_switch(self) -> bool:
        return self.digitalReadRuggeduino(2)

    @property
    def back_switch(self) -> bool:
        return self.digitalReadRuggeduino(3)

    @property
    def between_gripper_switch(self) -> bool:
        return self.digitalReadRuggeduino(4)

    @property
    def left_finger_switch(self) -> bool:
        return self.digitalReadRuggeduino(5)

    @property
    def right_finger_switch(self) -> bool:
        return self.digitalReadRuggeduino(6)

    @property
    def front_left_distance(self) -> float:
        return self.analogReadRuggeduinos(0)

    @property
    def front_right_distance(self) -> float:
        return self.analogReadRuggeduinos(1)

    @property
    def left_distance(self) -> float:
        return self.analogReadRuggeduinos(2)

    @property
    def right_distance(self) -> float:
        return self.analogReadRuggeduinos(3)

    @property
    def back_left_distance(self) -> float:
        return self.analogReadRuggeduinos(4)

    @property
    def back_right_distance(self) -> float:
        return self.analogReadRuggeduinos(5)

    def digitalReadRuggeduino(self, pin: int) -> bool:
        return self.ruggeduinos[0].digital_read(pin)

    def analogReadRuggeduinos(self, pin: int) -> float:
        return self.ruggeduinos[0].analogue_read(pin)

    def setDriveMotors(self, power: Union[float, Tuple[float, float]]):
        try:
            self.left_motor.power = power[0]
            self.right_motor.power = power[1]
        except:
            self.left_motor.power = power
            self.right_motor.power = power

    def stopDriveMotors(self):
        self.setDriveMotors(0)
        # self.left_motor.power = 0
        # self.right_motor.power = 0

    def turn(self, power, time):
        self.setDriveMotors((power, -power))
        self.sleep(time)
        self.stopDriveMotors()

    def raiseGripper(self):
        self.lift_motor.power = -100
        self.sleep(0.3)
        self.lift_motor.power = 0

    def lowerGripper(self):
        self.lift_motor.power = 100
        self.sleep(0.3)
        self.lift_motor.power = 0

    def closeGripper(self):
        self.gripper_motor.power = -100
        for i in range(10):
            if not (self.left_finger_switch and self.right_finger_switch):
                self.sleep(0.2)
            else:
                break
        else:
            print("No cube in gripper, opening gripper")
            self.openGripper()
            return False
        self.sleep(0.4)
        print("Got cube")
        return True

    def openGripper(self):
        self.gripper_motor.power = 100
        self.sleep(1)
        self.gripper_motor.power = 0

    def find_marker(self, code: int, markers=None):
        """Returns the marker object that has the given code if not returns None.
        The list of markers can be given if not R.see() will be used.
        """
        if markers == None:
            markers = self.see()
        for m in markers:
            if m.info.code == code:
                return m
        return None

    def turn_to_marker(self, code: int, epsilon: int = 2):
        """Turns to the marker of the given code and returns its object.
        Returns None if the cube cannot be seen.
        Epsilon is the accuracy at which the robot should be facing the marker at.
        e.g. When epsilon is 1 the angle the robot is facing when this function exits will be less than 1 but greater than -1."""
        m = self.find_marker(code)
        if m is None:
            print(f"ERROR: Cannot see marker {code}")
            return None
        while not (-epsilon < m.rot_y and m.rot_y < epsilon):
            self.turn(signum(m.rot_y) * 5, 0.001)
            m = self.find_marker(code)
            if m is None:
                print(f"ERROR: Can no longer see marker {code}")
                return None
        return m
    
    def turncont(self, power):
        self.setDriveMotors((power, -power))

    def find_markers(self, codes: list, markers=None):
        """Returns the marker object that has the given code if not returns None.
        The list of markers can be given if not R.see() will be used.
        """
        output = []
        if markers == None:
            markers = self.see()
        for m in markers:
            if m.info.code in codes:
                output.append(m)
        return output

    def seek_markersss(self, codes: list, power: int = 10, repeats: int = None, interval: float = 0.02):
        """Turns until the marker is found. Power to turn at and number of turns can be given.
        If repeats is None it will keep going forever until the marker is found.
        """
        m = self.find_markers(codes)
        while not m:
            self.turn(power)
            self.sleep(interval)
            self.stopDriveMotors()
            if repeats is not None:
                repeats -= 1
                if repeats <= 0:
                    print(
                        f"ERROR: Could not find marker {code} with in alloted steps")
                    break
            m = self.find_markers(codes)
        return m

    def seek_marker(self, code: int, power: int = 10, repeats: int = None, interval: float = 0.02):
        """Turns until the marker is found. Power to turn at and number of turns can be given.
        If repeats is None it will keep going forever until the marker is found.
        """
        m = self.find_marker(code)
        while m is None:
            self.turncont(power)
            self.sleep(interval)
            self.stopDriveMotors()
            if repeats is not None:
                repeats -= 1
                if repeats <= 0:
                    print(
                        f"ERROR: Could not find marker {code} with in alloted steps")
                    break
            m = self.find_marker(code)
        return m

    def drive_to_marker(self, code: int, dist: float = 0.3, power: int = 10, interval: float = 0.2, epsilon: int = 2):
        """Drives straight towards a marker of the given code and stops a given distance away.
        interval is the time between checking if the robot is facing the marker and driving.
        """
        m = self.turn_to_marker(code, epsilon=epsilon)
        if m is None:
            return m
        while m.dist > dist:
            self.setDriveMotors(power)
            self.sleep(interval)
            self.stopDriveMotors()
            m = self.turn_to_marker(code, epsilon=epsilon)
            if m is None:
                return m
        print(f"Done, {m.dist}m away")
        return m
    
    def shuffle(self, time):
        self.setDriveMotors(50)
        self.sleep(time)
        self.stopDriveMotors()
