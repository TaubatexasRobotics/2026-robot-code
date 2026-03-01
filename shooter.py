import rev
import wpimath.controller
from wpilib import SmartDashboard
import math  # ADICIONADO para converter graus -> radianos

gear_ratio = 11.52

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

class Shooter:
    def __init__(self):
        self.motor = rev.SparkMax(53, rev.SparkMax.MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()

        self.pid = wpimath.controller.PIDController(0.01, 0.0, 0.0)
        self.pid.setTolerance(0.1)
        self.encoder.setPosition(0)

        self.feedforward = wpimath.controller.ArmFeedforward(0.0, 0.5, 0.0, 0.0)  # ADICIONADO kG inicial = 0.05

    
    def getPosition(self) -> float:
        return self.encoder.getPosition() * gear_ratio * 360

    def update_dashboard(self):
        SmartDashboard.putData("PID", self.pid)
        SmartDashboard.putNumber("crest encoder", self.encoder.getPosition())
        SmartDashboard.putNumber("crest position", float(self.getPosition()))
        print(self.pid.getSetpoint())

    def move_to_setpoint(self):
        current_position = self.getPosition()
        motor_value = self.pid.calculate(current_position)

        angle_radians = math.radians(self.pid.getSetpoint())  # ADICIONADO conversão para feedforward
        ff = self.feedforward.calculate(angle_radians, 0)  # ADICIONADO cálculo do kG

        motor_value = motor_value + ff  # ADICIONADO soma do feedforward

        motor_value = clamp(motor_value, -0.4, 0.4)
        self.motor.set(motor_value)

    def move_to(self, setpoint):
        current_position = self.getPosition()
        motor_value = self.pid.calculate(current_position, setpoint)

        angle_radians = math.radians(setpoint)  # ADICIONADO conversão para feedforward
        ff = self.feedforward.calculate(angle_radians, 0)  # ADICIONADO cálculo do kG

        motor_value = motor_value + ff  # ADICIONADO soma do feedforward

        motor_value = clamp(motor_value, -0.4, 0.4)
        self.motor.set(motor_value)

    def up(self):
        self.move_to(20)

    def down(self):
        self.move_to(0)
        
    def subir(self):    
      self.motor.set(1)
    
    def descer(self):
        self.motor.set(-0.7)

    def stop(self):
        self.motor.stopMotor()