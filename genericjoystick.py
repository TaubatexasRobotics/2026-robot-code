from wpilib import GenericHID
from buttons import g_xbox_360

class GenericJoystick(GenericHID):
    def __init__(self, port: int) -> None:
        super().__init__(port)

        self.name = self.getName()

    def getA() -> bool:
        match self.name:
            "Xbox Controller"
