from math import pi
from wpilib import SerialPort

# Joystick
kJoystickDriverPort = 0
kJoystickCoDriverPort = 1

# Drivetrain
kLeftFrontId = 1
kLeftBackId = 2
kRightFrontId = 3
kRightBackId = 4

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
kWheelCircumference = kWheelDiameter * pi
kRotationToMeters = kWheelCircumference / kGearReduction
kEncoderPPR = 2048
kDistancePerPulse = kRotationToMeters / kEncoderPPR
kRotationsPerMinuteToMetersPerSeconds = kRotationsToMeters / 60

# Arduino
kBaudRate = 9600

# WS2812b LEDs
kLEDUSBPort = SerialPort.Port.kUSB1
