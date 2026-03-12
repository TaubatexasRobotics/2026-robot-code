from wpilib import Joystick
from commands2 import TimedCommandRobot, CommandScheduler, Command, ParallelCommandGroup, SequentialCommandGroup
from RampJoystick import RampJoystick
from phoenix5 import WPI_VictorSPX
from wpilib.drive import DifferentialDrive
from drivetrain import Drivetrain
import constants
from commands2.button import JoystickButton, POVButton

class MyRobot(TimedCommandRobot):

    driverJoystick: Joystick = Joystick(constants.kJoystickDriverPort)
    copilotJoystick : Joystick = Joystick(constants.kJoystickCoDriverPort)
    
    def combineAxis(self, joystick: RampJoystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRawAxis(left_axis)
        rightTrigger = joystick.getRawAxis(right_axis)
        return rightTrigger + leftTrigger
    
    def robotInit(self) -> None:
        self.driver_joystick = RampJoystick(constants.Kdriver_joystick,0.5,0.7,0.8,0.2)
        self.codriver_joystick = RampJoystick(constants.Kcodriver_joystick,0.5,0.7,0.8,0.2)
        self.drivetrain = Drivetrain()

        POVButton(self.driverJoystick, 0).whileTrue(
            self.intake.up()
        )

        POVButton(self.driverJoystick, 180).whileTrue(
            self.intake.down()
        )

        JoystickButton(self.driverJoystick, 3).toggleOnTrue(self.intake.colectGamePiece())

        JoystickButton(self.driverJoystick, 4).whileTrue(self.intake.releaseGamePiece())
        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineAxis(self.driverJoystick, 2, 3),
                lambda: self.driverJoystick.getRawAxis(0)
            )
        )

        #Copilot Joystick
        JoystickButton(self.copilotJoystick, 6).toggleOnTrue(
            ParallelCommandGroup(
                self.shooter.activateFlywheel(),
                self.led.blue()
            )
        )   

        self.indexer.setDefaultCommand(
             self.indexer.feedAxis(lambda: self.combineAxis(self.copilotJoystick, 2, 3))
        )

        self.turret.setDefaultCommand(
            self.turret.activateYaw(lambda: self.copilotJoystick.getRawAxis(0))
        )  
          
        # JoystickButton(self.copilotJoystick, 1).whileTrue(
            #     self.turret.followYawTag(self.turretCamera, self.led)
            # )
    

        POVButton(self.copilotJoystick, 180).toggleOnTrue(
            self.shooter.activateFlywheel100()
        )
        POVButton(self.copilotJoystick, 270).toggleOnTrue(
            self.shooter.activateFlywheel75()
        )
        POVButton(self.copilotJoystick, 0).toggleOnTrue(
            self.shooter.activateFlywheel50()
        )

        POVButton(self.copilotJoystick, 90).toggleOnTrue(
            self.shooter.hoodUp()
        )

        # self.autoChooser.addOption(
        #     "Drive Straight Path", DriveStraightPath(self.drivetrain, 5)
        # )
        # SmartDashboard.putData("Auto Chooser", self.autoChooser)

        
    def teleopInit(self) -> None:
        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineAxis(self.driver_joystick, 2, 3),
                lambda: self.driver_joystick.getRawAxis(0)
            ) 
        )

    def teleopPeriodic(self) -> None:    
        pass
        # self.drivetrain.arcadeDrive(self.joystick.getRampAxis(1), self.joystick.getRampAxis(0),False)
        #self.motor1.set(self.joystick.getRampAxis(1))
        #self.motor2.set(self.joystick.getRampAxis(0))