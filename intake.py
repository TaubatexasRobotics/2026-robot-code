import wpilib
import rev
import wpimath.controller
import constants
from phoenix5 import WPI_VictorSPX

class Intake:
    def __init__(self):
        self.motor = rev.SparkMax(constants.kIntakeAngleMotor, rev.SparkLowLevel.MotorType.kBrushless)
        self.track_motor = WPI_VictorSPX(constants.kIntakeTrackMotor)

        self.encoder = self.motor.getEncoder()

        # P=0.01 em graus: se errar 90°, dá 0.9 de força (90 * 0.01
        self.arm_pid = wpimath.controller.PIDController(0.006, 0.0, 0.0)
        self.arm_pid.setTolerance(0.1) # 1 grau de tolerância
        self.encoder.setPosition(0)

        wpilib.SmartDashboard.putNumber("Position", 0)
        self.position = wpilib.SmartDashboard.getNumber("Position", 0)

    def get_posicao_graus(self):
        wpilib.SmartDashboard.putNumber("Position", self.encoder.getPosition())

    def clockwise(self) -> None:
        self.motor.set(0.3)
    
    def counterClockwise(self) -> None:
        self.motor.set(-0.3)

    def stop(self) -> None:
        self.motor.set(0)

    def clockwiseTrack(self) -> None:
        self.track_motor.set(0.5)
    
    def counterClockwiseTrack(self) -> None:
        self.track_motor.set(-0.5)
    
    def stopTrack(self) -> None:
        self.track_motor.set(0)

    def testeMotor(self):
        setpoint = -220 
        posicao_atual = (self.encoder.getPosition() / 2.87) * 360
        
        output = self.arm_pid.calculate(posicao_atual, setpoint)
        
        # Limite de segurança
        output = max(min(output, 0.4), -0.4) 

        if not self.arm_pid.atSetpoint():
            self.motor.set(output)
        else:
            self.motor.set(0)
        
        print(f"Graus: {posicao_atual:.2f} | Out: {output:.2f}")

    def Contrario(self):
        setpoint = -30  # 1/4 de volta em graus
        posicao_atual = (self.encoder.getPosition() / 2.87) * 360
        
        output = self.arm_pid.calculate(posicao_atual, setpoint)
        
        # Limite de segurança
        output = max(min(output, 0.7), -0.7) 

        if not self.arm_pid.atSetpoint():
            self.motor.set(output)
        else:
            self.motor.set(0)
        
        print(f"Graus: {posicao_atual:.2f} | Out: {output:.2f}")

    def ativar(self, setpoint):
        posicao_atual = wpilib.SmartDashboard.putNumber("Position", 0) / 64
        output = self.arm_pid.calculate(posicao_atual, setpoint)  
        if not self.arm_pid.atSetpoint():
            self.motor.set(output)
        else:
            self.motor.set(0)
