import types
from enum import Enum

PNS = types.SimpleNamespace()

"""product category"""
PNS.PRODUCT_ID = b"AB"


class LEDColorUnit(Enum):
    """LED color unit for detailed control only"""

    RED = 0x01
    YELLOW = 0x02
    LEMON = 0x03
    GREEN = 0x04
    SKY_BLUE = 0x05
    BLUE = 0x06
    PURPLE = 0x07
    PEACH = 0x08
    WHITE = 0x09
    OFF = 0x00


class LEDUnit(Enum):
    OFF = 0x00
    ON = 0x01
    BLINKING = 0x02
    NO_CHANGE = 0x09


class BUZZERUnit(Enum):
    STOP = 0x00
    PATTERN1 = 0x01
    PATTERN2 = 0x02
    TONE = 0x03
    NO_CHANGE = 0x09


class BUZZERPattern(Enum):
    """buzzer pattern for detailed control only"""

    STOP = 0x00
    PATTERN1 = 0x01
    PATTERN2 = 0x02
    PATTERN3 = 0x03
    PATTERN4 = 0x04
    PATTERN5 = 0x05
    PATTERN6 = 0x06
    PATTERN7 = 0x07
    PATTERN8 = 0x08
    PATTERN9 = 0x09
    PATTERN10 = 0x0A
    PATTERN11 = 0x0B


class BLINKING(Enum):
    """blinking for detailed control only"""

    OFF = 0x00
    ON = 0x01


PNS.CONTROL = types.SimpleNamespace()
PNS.CONTROL.DETAIL = types.SimpleNamespace()

PNS.CONTROL.LED = LEDUnit
PNS.CONTROL.DETAIL.LED = LEDColorUnit

PNS.CONTROL.BUZZER = BUZZERUnit
PNS.CONTROL.DETAIL.BUZZER = BUZZERPattern


class PHNCONTROL(Enum):
    # action data of PHN command
    LED_UNIT1_BLINKING = 0x20
    """1st LED unit blinking"""
    LED_UNIT2_BLINKING = 0x40
    """2nd LED unit blinking"""
    LED_UNIT3_BLINKING = 0x80
    """3rd LED unit blinking"""
    BUZZER_PATTERN1 = 0x8
    """buzzer pattern 1"""
    BUZZER_PATTERN2 = 0x10
    """buzzer pattern 2"""
    LED_UNIT1_LIGHTING = 0x1
    """1st LED unit lighting"""
    LED_UNIT2_LIGHTING = 0x2
    """2nd LED unit lighting"""
    LED_UNIT3_LIGHTING = 0x4
    """3rd LED unit lighting"""


class MODE(Enum):
    """mode for detailed control only"""

    LED = 0x00
    SMART = 0x01
