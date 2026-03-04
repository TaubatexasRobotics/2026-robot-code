from math import pi
from wpilib import SerialPort
from wpimath.kinematics import DifferentialDriveKinematics
from rev import SparkLowLevel, FeedbackSensor, SparkBaseConfig, ClosedLoopSlot

# Joystick
kJoystickDriverPort = 0
kJoystickCoDriverPort = 1
kRealXboxController = "Controller (XBOX 360 For Windows)"
kSimXboxController = "Xbox Controller"
kGenericPS4Controller = "Wire PS4 Controller"

# Drivetrain Motor Controllers
kLeftFrontId = 50
kLeftBackId = 52
kRightFrontId = 55
kRightBackId = 54
kDrivetrainSmartCurrentLimit = 40
kDrivetrainMotorType = SparkLowLevel.MotorType.kBrushless
kDrivetrainIdleMode = SparkBaseConfig.IdleMode.kBrake
kDrivetrainPID = (0.2, 0, 0, ClosedLoopSlot.kSlot0)  # kP, kI, kD

# PhotonVision
kCameraName = "Camera7459"
kCameraHeightMeters = 0.83
kTargetHeightMeters = 1.12
kCameraPitchRadians = 0
kGoalRangeMeters = 1

# Limelight 3A
kLimelightRemoteHost = "172.29.0.1"
kLimelightPortForwarder = (
    5807,
    kLimelightRemoteHost,
    5807,
)  # port, remoteHost, remotePort

# Drivetrain Odometry
kInitialPose = (0, 0, 0)

# Drivetrain Kinematics
kTrackWidthMeters = 0.5
kDrivetrainKinematics = DifferentialDriveKinematics(kTrackWidthMeters)
kMaxVelocityMetersPerSecond = 3
kMaxAccelerationMetersPerSecondSquared = 1

# Drivetrain Encoders
kLeftMotorsInverted = False
kRightMotorsInverted = True
kWheelDiameter = 0.152  # HiGrip
kGearReduction = 10.7  # Toughbox Mini
kRotationsToMeters = (kWheelDiameter * pi) / kGearReduction
kRotationsPerMinuteToMetersPerSecond = kRotationsToMeters / 60
kFeedbackSensor = FeedbackSensor.kPrimaryEncoder

# Drivetrain Feedforward (kS = V, kV = V * s / m, kA = V * s^2 / m)
kDrivetrainFeedForward = (0.30329, 2.9096, 0.35543, ClosedLoopSlot.kSlot0)  # kS, kV, kA

# Arduino
kBaudRate = 9600

# WS2812b LEDs
kLEDUSBPort = SerialPort.Port.kUSB1

# Intake
kIntakeAngleId = 4
kIntakeTrackId = 1
kPivotTimeDown = 0.35
kPivotTimeUp = 0.5

# Shooter
kFlywheelId = 51
kFlywheelFeedForward = (0, 0, 0, ClosedLoopSlot.kSlot0)  # kS, kV, kA
kFlywheelPID = (0.2, 0.1, 0, ClosedLoopSlot.kSlot0)  # kP, kI, kD
kHoodId = 53

# Indexer
kFrontRoller = 5 # 775 RedLine
kBackRoller = 2

# Turret
kTurretId = 56