import rev
import wpimath.controller
from wpilib import SmartDashboard

gear_ratio = 11.52

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

class Crest:
    def __init__(self):
        self.motor = rev.SparkMax(53, rev.SparkMax.MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()

        self.pid = wpimath.controller.PIDController(0.006, 0.0, 0.0)
        self.pid.setTolerance(0.1)
        self.encoder.setPosition(0)


    def getPosition(self) -> float:
        return self.encoder.getPosition() * gear_ratio * 360

    def update_dashboard(self):
        SmartDashboard.putData("PID", self.pid)
        SmartDashboard.putNumber("crest encoder", self.encoder.getPosition())
        SmartDashboard.putNumber("crest position", float(self.getPosition()))
        # self.pid.setSetpoint(self.setpoint)
        print(self.pid.getSetpoint())

    def move_to_setpoint(self):
        current_position = self.getPosition()
        motor_value = self.pid.calculate(current_position)
        motor_value = clamp(motor_value, -0.4, 0.4)
        self.motor.set(motor_value)

    def move_to(self, setpoint):
        current_position = self.getPosition()
        motor_value = self.pid.calculate(current_position, setpoint)
        motor_value = clamp(motor_value, -0.4, 0.4)
        self.motor.set(motor_value)

    def up(self):
        self.move_to(20)

    def down(self):
        self.move_to(0)
        
    def subir(self):    
      self.motor.set(0.2)
    
    def descer(self):
        self.motor.set(-0.05)

    def stop(self):
        self.motor.stopMotor()
