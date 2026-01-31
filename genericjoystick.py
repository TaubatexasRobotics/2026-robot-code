from wpilib.interfaces import GenericHID
from buttons import g_xbox_360_map, g_ps4_controller
import constants

class GenericJoystick(GenericHID):   
    def __init__(self, port: int) -> None:
        super().__init__(port)

        self.name = self.getName()

    def getA(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['cross'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['a'])
        return False
    
    def getB(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['circle'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['b'])
        return False
            
    def getX(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['square'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['x'])
        return False
            
    def getY(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['triangle'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['y'])
        return False
            
    def getLeftBumper(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['l1'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['lb'])
        return False
            
    def getRightBumper(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['r1'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['rb'])
        return False
    
    def getBack(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['share'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['back'])
    
    def getStart(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['options'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['start'])
    
    def getL_stick(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['l3'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['press_left_stick'])
    
    def getR_stick(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['r3'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['press_right_stick'])
    
    def getPov_up(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['pov-up'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['pov-up'])
    
    def getPov_down(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['pov-down'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['pov-down'])
    
    def getPov_left(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['pov-left'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['pov-left'])
    
    def getPov_right(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller['pov-right'])
            case constants.kXboxController:
                return self.getRawButton(g_xbox_360_map['pov-right'])
    
    def getLeftXAxis(self) -> float:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller['left-x-axis'])
            case constants.kXboxController:
                return self.getRawAxis(g_xbox_360_map['left-x-axis'])
        return 0
    
    def getLeftYAxis(self) -> float:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller['left-y-axis'])
            case constants.kXboxController:
                return self.getRawAxis(g_xbox_360_map['left-y-axis'])
        return 0
    
    def getRightXAxis(self) -> float:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller['right-x-axis'])
            case constants.kXboxController:
                return self.getRawAxis(g_xbox_360_map['right-x-axis'])
        return 0
    
    def getRightYAxis(self) -> float:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller['right-y-axis'])
            case constants.kXboxController:
                return self.getRawAxis(g_xbox_360_map['right-y-axis'])
        return 0
    
    def getL_trigger_axis(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller['left-trigger-axis'])
            case constants.kXboxController:
                return self.getRawAxis(g_xbox_360_map['left-trigger-axis'])
    
    def getR_trigger_axis(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller['right-trigger-axis'])
            case constants.kXboxController:
                return self.getRawAxis(g_xbox_360_map['right-trigger-axis'])
    
    def getY(self) -> bool:
        match self.name:
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller['triangle'])
            case constants.kXboxController:
                return self.getRawAxis(g_xbox_360_map['y'])
