from wpilib import Joystick
from wpimath.trajectory import TrapezoidProfile

class RampJoystick(Joystick):
    def __init__(self, port, minRevertionSetpoint, minStopSetpoint, maxSetpoint, deadZone):
        super().__init__(port)

        self.constraints = TrapezoidProfile.Constraints(
            maxVelocity = 1.0,      
            maxAcceleration=5.0  
        )

        self.profile = TrapezoidProfile(self.constraints)

        self.minRevertionSetpoint = minRevertionSetpoint
        self.minStopSetpoint = minStopSetpoint
        self.maxSetpoint = maxSetpoint
        self.deadZone = deadZone

        self.dt = 0.02

        self.currentState0 = TrapezoidProfile.State(0)
        self.currentState1 = TrapezoidProfile.State(0)
        self.currentState2 = TrapezoidProfile.State(0)
        self.currentState3 = TrapezoidProfile.State(0)
        self.currentState4 = TrapezoidProfile.State(0)
        self.currentState5 = TrapezoidProfile.State(0)

    def getCurrentState(self, slot:int):
        match slot:
            case 0:
                return self.currentState0
            case 1:
                return self.currentState1
            case 2:
                return self.currentState2
            case 3:
                return self.currentState3
            case 4:
                return self.currentState4
            case 5:
                return self.currentState5
    
    def setCurrentState(self, slot:int, state: TrapezoidProfile.State):
        match slot:
            case 0:
                self.currentState0 = state
            case 1:
                self.currentState1 = state
            case 2:
                self.currentState2 = state
            case 3:
                self.currentState3 = state
            case 4:
                self.currentState4 = state
            case 5:
                self.currentState5 = state

    def getRampAxis(self, joystickAxis: int): 

        if  ((self.getCurrentState(joystickAxis).position > 0 and self.getRawAxis(joystickAxis) < 0) or (self.getCurrentState(joystickAxis).position < 0 and self.getRawAxis(joystickAxis) > 0)):
            if self.getCurrentState(joystickAxis).position > self.minRevertionSetpoint or self.getCurrentState(joystickAxis).position < -self.minRevertionSetpoint:        
                goal = TrapezoidProfile.State(0)

                self.setCurrentState(joystickAxis, self.profile.calculate(self.dt, self.getCurrentState(joystickAxis), goal))
                
                return self.getCurrentState(joystickAxis).position*self.maxSetpoint
            else:
                self.setCurrentState(joystickAxis,TrapezoidProfile.State(0))
                return 0
                
        #Dead zone que irá mandar freiar o robô
        elif self.getRawAxis(joystickAxis) > self.deadZone or self.getRawAxis(joystickAxis) < - self.deadZone:
    
                goal = TrapezoidProfile.State(self.getRawAxis(joystickAxis))

                self.setCurrentState(joystickAxis,self.profile.calculate(self.dt, self.getCurrentState(joystickAxis), goal))

                return self.getCurrentState(joystickAxis).position*self.maxSetpoint

        #Freio do robo
        else:
            if self.getCurrentState(joystickAxis).position > self.minStopSetpoint or self.getCurrentState(joystickAxis).position < -self.minStopSetpoint:        
                goal = TrapezoidProfile.State(0)

                self.setCurrentState(joystickAxis,self.profile.calculate(self.dt, self.getCurrentState(joystickAxis), goal))

                return self.getCurrentState(joystickAxis).position*self.maxSetpoint
            else:
                self.setCurrentState(joystickAxis,TrapezoidProfile.State(0))
                return 0
