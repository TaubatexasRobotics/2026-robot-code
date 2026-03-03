import rev
import wpimath.controller
from wpilib import SmartDashboard
from commands2 import Subsystem, command


gear_ratio = 11.52

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

class Crest(Subsystem):
    def __init__(self):
        self.motor = rev.SparkMax(53, rev.SparkMax.MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()

        self.pid = wpimath.controller.PIDController(0.006, 0.0, 0.0)
        self.pid.setTolerance(0.1)
        self.encoder.setPosition(0)

    
    def getPosition(self) -> float:
        return self.encoder.getPosition() * gear_ratio * 360

    def updateDashboard(self):
        SmartDashboard.putData("PID", self.pid)
        SmartDashboard.putNumber("crest encoder", self.encoder.getPosition())
        SmartDashboard.putNumber("crest position", float(self.getPosition()))
        # self.pid.setSetpoint(self.setpoint)
        print(self.pid.getSetpoint())

    def moveToSetpoint(self):
        current_position = self.getPosition()
        motor_value = self.pid.calculate(current_position)
        motor_value = clamp(motor_value, -0.4, 0.4)
        self.motor.set(motor_value)

    def commandMoveToSetpoint(self) -> command:
        return self.run(lambda: self.moveToSetpoint)

    def moveTo(self, setpoint):
        current_position = self.getPosition()
        motor_value = self.pid.calculate(current_position, setpoint)
        motor_value = clamp(motor_value, -0.4, 0.4)
        self.motor.set(motor_value)

    def up(self):
        self.moveTo(20)

    def down(self):
        self.moveTo(0)
        
    def subir(self):    
      self.motor.set(0.2)
    
    def descer(self):
        self.motor.set(-0.05)

    def stop(self):
        self.motor.stopMotor()