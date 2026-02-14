from wpilib.interfaces import GenericHID
from buttons import g_xbox_360_map, g_ps4_controller
import constants


class GenericJoystick(GenericHID):
    def __init__(self, port: int) -> None:
        super().__init__(port)

    def getA(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["cross"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["a"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["a"])
        return False

    def getB(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["circle"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["b"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["b"])
        return False

    def getX(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["square"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["x"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["x"])
        return False

    def getY(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["triangle"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["y"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["y"])
        return False

    def getLeftBumper(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["l1"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["lb"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["lb"])
        return False

    def getRightBumper(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["r1"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["rb"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["rb"])
        return False

    def getBack(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["share"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["back"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["back"])
        return False

    def getStart(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["options"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["start"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["start"])
        return False

    def getLeftStick(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["l3"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["press-left-stick"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["press-left-stick"])
        return False

    def getRightStick(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawButton(g_ps4_controller["r3"])
            case constants.kRealXboxController:
                return self.getRawButton(g_xbox_360_map["press-right_stick"])
            case constants.kSimXboxController:
                return self.getRawButton(g_xbox_360_map["press-right-stick"])
        return False

    def getPOVUp(self) -> int:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getPOV(g_ps4_controller["pov-up"])
            case constants.kRealXboxController:
                return self.getPOV(g_xbox_360_map["pov-up"])
            case constants.kSimXboxController:
                return self.getPOV(g_xbox_360_map["pov-up"])
        return -1

    def getPOVDown(self) -> int:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getPOV(g_ps4_controller["pov-down"])
            case constants.kRealXboxController:
                return self.getPOV(g_xbox_360_map["pov-down"])
            case constants.kSimXboxController:
                return self.getPOV(g_xbox_360_map["pov-down"])
        return -1

    def getPOVLeft(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getPOV(g_ps4_controller["pov-left"])
            case constants.kRealXboxController:
                return self.getPOV(g_xbox_360_map["pov-left"])
            case constants.kSimXboxController:
                return self.getPOV(g_xbox_360_map["pov-left"])
        return -1

    def getPOVRight(self) -> bool:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getPOV(g_ps4_controller["pov-right"])
            case constants.kRealXboxController:
                return self.getPOV(g_xbox_360_map["pov-right"])
            case constants.kSimXboxController:
                return self.getPOV(g_xbox_360_map["pov-right"])
        return -1

    def getLeftXAxis(self) -> float:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller["left-x-stick"])
            case constants.kRealXboxController:
                return self.getRawAxis(g_xbox_360_map["left-x-stick"])
            case constants.kSimXboxController:
                return self.getRawAxis(g_xbox_360_map["left-x-stick"])
        return 0

    def getLeftYAxis(self) -> float:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller["left-y-stick"])
            case constants.kRealXboxController:
                return self.getRawAxis(g_xbox_360_map["left-y-stick"])
            case constants.kSimXboxController:
                return self.getRawAxis(g_xbox_360_map["left-y-stick"])
        return 0

    def getRightXAxis(self) -> float:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller["right-x-stick"])
            case constants.kRealXboxController:
                return self.getRawAxis(g_xbox_360_map["right-x-stick"])
            case constants.kSimXboxController:
                return self.getRawAxis(g_xbox_360_map["right-x-stick"])
        return 0

    def getRightYAxis(self) -> float:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller["right-y-stick"])
            case constants.kRealXboxController:
                return self.getRawAxis(g_xbox_360_map["right-y-stick"])
            case constants.kSimXboxController:
                return self.getRawAxis(g_xbox_360_map["right-y-stick"])
        return 0

    def getLeftTriggerAxis(self) -> float:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller["left-trigger-axis"])
            case constants.kRealXboxController:
                return self.getRawAxis(g_xbox_360_map["left-trigger-axis"])
            case constants.kSimXboxController:
                return self.getRawAxis(g_xbox_360_map["left-trigger-axis"])
        return 0

    def getRightTriggerAxis(self) -> float:
        match self.getName():
            case constants.kGenericPS4Controller:
                return self.getRawAxis(g_ps4_controller["right-trigger-axis"])
            case constants.kRealXboxController:
                return self.getRawAxis(g_xbox_360_map["right-trigger-axis"])
            case constants.kSimXboxController:
                return self.getRawAxis(g_xbox_360_map["right-trigger-axis"])
        return 0
