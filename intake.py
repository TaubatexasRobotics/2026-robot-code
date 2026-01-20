import wpilib
import wpilib.drive
import rev
import wpimath.controller


class Intake:

    def __init__(self):

        self.arm_motor = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.roller_motor = rev.SparkMax(2, rev.SparkLowLevel.MotorType.kBrushless)

        self.arm_pid = wpimath.controller.PIDController(0.1, 0.0, 0.0)

        
    def turnOnIntake(self):
        setpoint = 15
        self.roller_motor.set(1)

        while not self.arm_pid.inSetPoint:
            self.arm_motor.set(self.arm_pid.calculate(self.arm_motor.getEncoder().getPosition(), setpoint))

    def turnOffIntake(self):
        setpoint = 0
        self.roller_motor.set(0) 

        while not self.arm_pid.inSetPoint:
            self.arm_motor.set(self.arm_pid.calculate(self.arm_motor.getEncoder().getPosition(), setpoint))
         



       
