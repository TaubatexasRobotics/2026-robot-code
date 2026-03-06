import rev
import phoenix5
from wpilib import XboxController, SmartDashboard

FLYWHEEL_MOTOR_ID = 51
PRESHOOTER_MOTOR_ID = 2
FLYWHEEL_MAX_SPEED = 1

PRESHOOTER_SPEED = 0.5
PRESHOOTER_RELEASE_SPEED = -1

class Shooter():  
    def __init__(self):
        self.flywheel_motor = rev.SparkMax(FLYWHEEL_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.preshooter_motor = phoenix5.WPI_VictorSPX(PRESHOOTER_MOTOR_ID)
        self.flywheel_encoder = self.flywheel_motor.getEncoder()

        self.is_enabled = False
        self.joystick = XboxController(1)
        
    def update_dashboard(self):
        SmartDashboard.putBoolean("Indexer/preshooter moving", self.preshooter_motor.get())
        SmartDashboard.putNumber("Indexer/preshooter", self.preshooter_motor.get())
        
        SmartDashboard.putBoolean("Shooter/flywheel enabled", self.is_enabled)
        SmartDashboard.putBoolean("Shooter/flywheel moving", self.is_enabled)
        SmartDashboard.putBoolean("Shooter/flywheel", self.flywheel_motor.get())
        SmartDashboard.putNumber("Shooter/flywheel velocity", self.flywheel_encoder.getVelocity())
    
    def send_to_flywheel(self) -> None:
        self.preshooter_motor.set(PRESHOOTER_SPEED)
        
    def stop_preshooter(self) -> None:
        self.preshooter_motor.set(0)
        
    def reverse_preshooter(self) -> None:
        self.preshooter_motor.set(PRESHOOTER_RELEASE_SPEED)
        
    def teleopPeriodic(self):
        if self.joystick.getRightBumperButtonPressed():
            self.is_enabled = not self.is_enabled
            
        if self.joystick.getLeftBumperButton():
            self.flywheel_motor.set(-1)
            self.is_enabled = False
            
        if self.is_enabled:
            self.flywheel_motor.set(FLYWHEEL_MAX_SPEED)
            self.joystick.setRumble(XboxController.RumbleType.kBothRumble, 0.5)
        else:
            self.flywheel_motor.set(0)
            self.joystick.setRumble(XboxController.RumbleType.kBothRumble, 0)
            
        if self.joystick.getRightTriggerAxis() > 0.5:
            self.send_to_flywheel()
        else:
            self.stop_preshooter()
            
        if self.joystick.getLeftTriggerAxis() > 0.5:
            self.reverse_preshooter()