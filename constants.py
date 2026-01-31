from math import pi
from wpilib import SerialPort
from pathplannerlib.config import RobotConfig, ModuleConfig

# Joystick
kJoystickDriverPort = 0
kJoystickCoDriverPort = 1
kXboxController = "Controller (XBOX 360 For Windows)"
kGenericPS4Controller = "Wire PS4 Controller"

# Drivetrain
kLeftFrontId = 50
kLeftBackId = 52
kRightFrontId = 55
kRightBackId = 54
kSparkMaxSmartCurrentLimit = 40

# PhotonVision
kCameraName = "Camera7459"
kCameraHeightMeters = 0.83
kTargetHeightMeters = 1.12
kCameraPitchRadians = 0
kGoalRangeMeters = 1

# Drivetrain Odometry
kInitialPose = (0, 0, 0)

# Drivetrain Kinematics
kTrackWidthInMeters = 0.5

# Drivetrain PID Controller
kPIDAngularDrivetrain = (0.1, 0, 0)
kPIDForwardDrivetrain = (0.1, 0, 0)

# Drivetrain Encoders
kLeftEncoder = (1, 2)
kRightEncoder = (3, 4, True)
kWheelDiameter = 0.152 # HiGrip
kGearReduction = 10.7 # Toughbox Mini

# Arduino
kBaudRate = 9600

# WS2812b LEDs
kLEDUSBPort = SerialPort.Port.kUSB1

# Intake
kIntakeAngleMotor = 53
kIntakeTrackMotor = 1