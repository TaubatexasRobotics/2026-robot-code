from wpimath.controller import PIDController

# Joysticks
Kdriver_joystick = 0
Kcodriver_joystick = 1

# Drivetrain
Kleft_front_id = 4
Kleft_back_id = 2
Kright_front_id = 5
Kright_back_id = 1

Kdrivetrain_PID = PIDController(0.2, 0, 0)

# Intake
Kintake_pivot_id = 52
Kintake_roller_id = 1

Kintake_PID = PIDController(0.2, 0, 0)

# Generic Xbox 360 Controller
g_xbox_360_map = {
    "a": 1,
    "b": 2,
    "x": 3,
    "y": 4,
    "lb": 5,
    "rb": 6,
    "back": 7,
    "start": 8,
    "press-left-stick": 9,
    "press-right-stick": 10,
    "pov-up": 0,
    "pov-down": 180,
    "pov-left": 270,
    "pov-right": 90,
    "left-x-stick": 0,
    "left-y-stick": 1,
    "left-trigger-axis": 2,
    "right-trigger-axis": 3,
    "right-y-stick": 5,
    "right-x-stick": 4,
}