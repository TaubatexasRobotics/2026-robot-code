from utils import clamp
import rev
from wpimath.controller import PIDController, ArmFeedforward
from wpilib import SmartDashboard, XboxController

gear_ratio = 11.52
HOOD_MOTOR_ID = 53

MIN_VOLTAGE = -7
MAX_VOLTAGE = 7

class Hood:
    def __init__(self):
        self.motor = rev.SparkMax(HOOD_MOTOR_ID, rev.SparkMax.MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()

        self.pid = PIDController(.006, .0, .0)
        self.ff = ArmFeedforward(.0, .0, .0, .0)
        self.pid.setTolerance(0.1)
        self.encoder.setPosition(0)
        
        # TODO: set controller to 1 for copilot
        self.joystick = XboxController(1)
        
        SmartDashboard.putNumber("Hood/set voltage", 7)
        
        
    def set_position(self, position):
        self.encoder.setPosition(position)

    def get_angle(self) -> float:
        return self.encoder.getPosition() * gear_ratio * 360
    
    def get_angle_radians(self) -> float:
        return self.get_angle() * 3.1415926535 / 180
      
    def get_velocity(self) -> float:
        return self.encoder.getVelocity() * gear_ratio * 360 / 60

    def update_dashboard(self):
        SmartDashboard.putData("Hood/PID", self.pid)
        SmartDashboard.putNumber("Hood/read voltage", self.get_voltage())
        SmartDashboard.putNumber("Hood/encoder", self.motor.getEncoder().getPosition())
        SmartDashboard.putNumber("Hood/angle", self.get_angle())
        SmartDashboard.putNumber("Hood/motor", self.motor.get())
        
        SmartDashboard.putNumber("Hood/FF/Ka", self.ff.getKa())
        SmartDashboard.putNumber("Hood/FF/Kg", self.ff.getKg())
        SmartDashboard.putNumber("Hood/FF/Kv", self.ff.getKv())
        SmartDashboard.putNumber("Hood/FF/Ks", self.ff.getKs())
        
        
    def set_voltage(self, voltage):
        self.motor.setVoltage(voltage)
        
    def get_voltage(self):
        # I don't know if this works
        return self.motor.getAppliedOutput() * self.motor.getBusVoltage()
    
    def move_to_setpoint(self):
        ff = self.ff.calculate(self.get_angle_radians(), self.get_velocity())
        pid = self.pid.calculate(self.get_angle_radians())
        motor_voltage = clamp(ff + pid, MIN_VOLTAGE, MAX_VOLTAGE)
        self.motor.setVoltage(motor_voltage)

    def move_to(self, setpoint):
        '''Moves the Hood to the given angle in radians.'''
        self.pid.setSetpoint(setpoint)
        self.move_to_setpoint()
        
    def teleopPeriodic(self):
        
        y_value = float(self.joystick.getRightY())
        if 0.1 > y_value > -0.1:
            self.motor.set(0)
        else:
            self.motor.set(y_value)
        
        # voltage = SmartDashboard.getNumber("Hood/set voltage", 0)
        # if voltage != 0:
        #     self.set_voltage(voltage)
        # else:
        #     self.move_to_setpoint()