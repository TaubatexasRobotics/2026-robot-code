import wpilib
import rev
import wpimath.controller

class Crest:
    def __init__(self):
        self.crest_motor = rev.SparkMax(55, rev.SparkMax.MotorType.kBrushless)
        self.encoder = self.crest_motor.getEncoder()

        self.crest_pid = wpimath.controller.PIDController(0.006, 0.0, 0.0)
        self.crest_pid.setTolerance(0.1)
        self.encoder.setPosition(0)

    def get_posicao_graus(self):
        return (self.encoder.getPosition() * 11,52 / 360)

    def testeMotor(self):
        setpoint = 20 #graus
        posicao_atual = (self.encoder.getPosition() * 11,52 / 360)
              
        output = self.crest_pid.calculate(posicao_atual, setpoint)
        
        # Limite de segurança
        output = max(min(output, 0.4), -0.4) 

        if not self.crest_pid.atSetpoint():
            self.crest_motor.set(output)
        else:
            self.crest_motor.set(0)
        
        print(f"Graus: {posicao_atual:.2f} | Out: {output:.2f}")

    def Contrario(self):
        setpoint = 0  # 1/4 de volta em graus
        posicao_atual = (self.encoder.getPosition() * 11,52 / 360)
      
        
        output = self.crest_pid.calculate(posicao_atual, setpoint)
        
        # Limite de segurança
        output = max(min(output, 0.4), -0.4) 

        if not self.crest_pid.atSetpoint():
            self.crest_motor.set(output)
        else:
            self.crest_motor.set(0)
        
        print(f"Graus: {posicao_atual:.2f} | Out: {output:.2f}")
        
    def subir(self):    
      self.crest_motor.set(0.2)
    
    def descer(self):
        self.crest_motor.set(-0.05)
    def parar(self):
        self.crest_motor.set(0)