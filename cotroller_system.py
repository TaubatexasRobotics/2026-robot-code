import wpilib
import ntcore

class TRobot(wpilib.TimedRobot):

    def robotInit(self):
        inst = ntcore.NetworkTableInstance.getDefault()

        mesa = inst.getTable("IDK")

        t = mesa.putNumber("x/a", 1)

        match t:
            case 1:
                return 
            case 2:
                return 1