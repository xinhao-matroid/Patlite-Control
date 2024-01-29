import struct
from abc import ABC, abstractmethod
from .constants import MODE, PNS


class PatliteData(ABC):
    pass


class PNSCommandData(PatliteData):
    @abstractmethod
    def pack(self) -> bytes:
        pass

    @abstractmethod
    def data_size(self) -> int:
        pass

    def __str__(self) -> str:
        return f"data_size: {self.data_size()}, data: {self.pack()}"


class PNSResponseData(PatliteData):
    pass


class PNSStateData(PatliteData):
    pass


class EmptyData(PatliteData):
    def pack(self) -> bytes:
        return b""

    def data_size(self) -> int:
        return 0


class GeneralData(PatliteData):
    """
    Pack any data and send it to the Patlite
    """

    def __init__(self, run_data: int) -> None:
        self.run_data = run_data

    def pack(self):
        return struct.pack("B", self.run_data)

    def data_size(self) -> int:
        raise RuntimeError("This should never be called")


### Command Data Classes ###


class SmartModeCommandData(PNSCommandData):
    """
    Parameters
    ----------
    run_data: int
        Group number to execute smart mode (0x01(Group No.1) to 0x1F(Group No.31))
    """

    def __init__(self, run_data: int) -> None:
        self.run_data = run_data

    def pack(self):
        return struct.pack("B", self.run_data)

    def data_size(self) -> int:
        return 1


class StopPulseInputCommandData(PNSCommandData):
    """
    Parameters
    ----------
    input_mode: int
        STOP input/trigger input (STOP input ON/trigger input: 1, STOP input: 0)
    """

    def __init__(self, input_mode: int) -> None:
        self.input_mode = input_mode

    def pack(self):
        return struct.pack("B", self.input_mode)

    def data_size(self) -> int:
        return 1


class MuteCommandData(PNSCommandData):
    """
    Parameters
    ----------
    mute: int
        Buzzer ON/OFF (ON: 1, OFF: 0)
    """

    def __init__(self, mute: int) -> None:
        self.mute = mute

    def pack(self):
        return struct.pack("B", self.mute)

    def data_size(self) -> int:
        return 1


LED_CONTROL = PNS.CONTROL.LED
BUZZER_CONTROL = PNS.CONTROL.BUZZER


class RunControlCommandData(PNSCommandData):
    """operation control data class

    Parameters
    ----------
    run_control_data: PnsRunControlData
        LEDPattern of the 1st to 5th stage of the LED unit and buzzer (1 to 3)
        Pattern of LED unit (off: 0, on: 1, blinking: 2, no change: 9)
        Pattern of buzzer (stop: 0, pattern 1: 1, pattern 2: 2, buzzer tone when input simultaneously with buzzer: 3, no change: 9)
    """

    def __init__(
        self,
        led1_pattern: LED_CONTROL,
        led2_pattern: LED_CONTROL,
        led3_pattern: LED_CONTROL,
        led4_pattern: LED_CONTROL,
        led5_pattern: LED_CONTROL,
        buzzer_pattern: BUZZER_CONTROL,
    ):
        self._led1_pattern = led1_pattern
        self._led2_pattern = led2_pattern
        self._led3_pattern = led3_pattern
        self._led4_pattern = led4_pattern
        self._led5_pattern = led5_pattern
        self._buzzer_pattern = buzzer_pattern

    def pack(self) -> bytes:
        """
        Get the binary data of the operation control data.

        Returns
        -------
        data: bytes
            Binary data of operation control data
        """
        data = struct.pack(
            "BBBBBB",  # format
            self._led1_pattern.value,  # 1st LED unit pattern
            self._led2_pattern.value,  # 2nd LED unit pattern
            self._led3_pattern.value,  # 3rd LED unit pattern
            self._led4_pattern.value,  # 4th LED unit pattern
            self._led5_pattern.value,  # 5th LED unit pattern
            self._buzzer_pattern.value,  # buzzer pattern 1 to 3
        )
        return data

    def data_size(self) -> int:
        return 6


DETAIL_LED_CONTROL = PNS.CONTROL.DETAIL.LED
DETAIL_BUZZER_CONTROL = PNS.CONTROL.DETAIL.BUZZER


class DetailRunControlCommandData(PNSCommandData):
    """detail operation control data class

    Parameters
    ----------
    detail_run_control_data: PnsDetailRunControlData
        Pattern of the 1st to 5th stage of the LED unit, blinking operation and buzzer (1 to 3)
        Pattern of LED unit (off: 0, red: 1, yellow: 2, lemon: 3, green: 4, sky blue: 5, blue: 6, purple: 7, peach: 8, white: 9)
        Flashing action (Flashing OFF: 0, Flashing ON: 1)
        Buzzer pattern (Stop: 0, Pattern 1: 1, Pattern 2: 2, Pattern 3: 3, Pattern 4: 4, Pattern 5: 5, Pattern 6: 6, Pattern 7: 7, Pattern 8: 8, Pattern 9: 9, Pattern 10: 10, Pattern 11: 11)
    """

    def __init__(
        self,
        led1_color: DETAIL_LED_CONTROL,
        led2_color: DETAIL_LED_CONTROL,
        led3_color: DETAIL_LED_CONTROL,
        led4_color: DETAIL_LED_CONTROL,
        led5_color: DETAIL_LED_CONTROL,
        blinking_control: int,
        buzzer_pattern: DETAIL_BUZZER_CONTROL,
    ):
        self._led1_color = led1_color
        self._led2_color = led2_color
        self._led3_color = led3_color
        self._led4_color = led4_color
        self._led5_color = led5_color
        self._blinking_control = blinking_control
        self._buzzer_pattern = buzzer_pattern

    def pack(self):
        """
        Get the binary data of the detail operation control data.

        Returns
        -------
        data: bytes
            Binary data of detail operation control data
        """
        data = struct.pack(
            "BBBBBBB",  # format
            self._led1_color.value,  # 1st color of LED unit
            self._led2_color.value,  # 2nd color of LED unit
            self._led3_color.value,  # 3rd color of LED unit
            self._led4_color.value,  # 4th color of LED unit
            self._led5_color.value,  # 5th color of LED unit
            self._blinking_control,  # blinking action
            self._buzzer_pattern.value,  # buzzer pattern 1 to 11
        )
        return data

    def data_size(self) -> int:
        return 7


class PasswordCommandData(PNSCommandData):
    """password data class

    Parameters
    ----------
    password_data: PnsPasswordData
        Password for setting
    """

    def __init__(self, password: str):
        self._password = password

    def pack(self) -> bytes:
        return self._password.encode("ascii")

    def data_size(self) -> int:
        return len(self._password)


### Response Data ###
class StatusResponseData(PNSResponseData):
    """status data of operation control"""

    def __init__(self, data: bytes):
        """
        status data of operation control

        Parameters
        ----------
        data: bytes
            Response data for get status command
        """
        self._input = data[0:8]
        self._mode = MODE(int(data[8]))
        self._smart_mode_data = None
        self._led_mode_data = None

        if self._mode == MODE.LED:
            # signal light mode
            self._led_mode_data = LedModeStateData(data[9:])
        elif self._mode == MODE.SMART:
            # smart mode
            self._smart_mode_data = SmartModeStateData(data[9:])
        else:
            raise RuntimeError("Invalid mode: {}".format(self._mode))

    @property
    def input(self) -> bytes:
        """input 1 to 8"""
        return self._input[:]

    @property
    def mode(self) -> int:
        """mode"""
        return self._mode

    @property
    def led_mode_data(self) -> "LedModeStateData":
        """status data when running signal light mode"""
        return self._led_mode_data

    @property
    def smart_mode_data(self) -> "SmartModeStateData":
        """status data during smart mode execution"""
        return self._smart_mode_data

    def __str__(self):
        return "StatusResponseData(input={}, mode={}, led_mode_data={}, smart_mode_data={})".format(
            self._input, self._mode, self._led_mode_data, self._smart_mode_data
        )


class DetailStatusResponseData(PNSResponseData):
    """status data of detailed operation control"""

    def __init__(self, data: bytes):
        """
        status data of detailed operation control

        Parameters
        ----------
        data: bytes
            Response data for get detail status command
        """
        self._mac_address = data[0:6]
        self._input = data[6:14]
        self._mode = MODE(int(data[14]))
        self._smart_mode_detal_data = None
        self._led_mode_detal_data = None

        if self._mode == MODE.LED:
            # signal light mode
            self._led_mode_detal_data = LEDModeDetailStateData(data[19:])
        elif self._mode == MODE.SMART:
            # smart mode
            self._smart_mode_detal_data = SmartModeDetailStateData(data[19:])
        else:
            raise RuntimeError("Invalid mode: {}".format(self._mode))

    @property
    def mac_address(self) -> bytes:
        """MAC address"""
        return self._mac_address[:]

    def mac_addresss_str(self) -> str:
        """MAC address string"""
        return ":".join("{:02x}".format(x) for x in self._mac_address)

    @property
    def input(self) -> bytes:
        """Input 1 to 8"""
        return self._input[:]

    @property
    def mode(self) -> int:
        """mode"""
        return self._mode

    @property
    def led_mode_detail_data(self) -> "LEDModeDetailStateData":
        """detailed status data when running signal light mode"""
        return self._led_mode_detal_data

    @property
    def smart_mode_detail_data(self) -> "SmartModeDetailStateData":
        """detailed state data when running in smart mode"""
        return self._smart_mode_detal_data

    def __str__(self):
        return "DetailStatusResponseData(mac_address={}, input={}, mode={}, led_mode_detail_data={}, smart_mode_detail_data={})".format(
            self.mac_addresss_str(),
            [str(i) for i in self._input],
            self._mode,
            self._led_mode_detal_data,
            self._smart_mode_detal_data,
        )


### State Data ###
class LedModeStateData(PNSStateData):
    """status data when running in signal light mode"""

    def __init__(self, data: bytes):
        """
        status data when running in signal light mode

        Parameters
        ----------
        data: bytes
            LED unit/buzzer patterns" portion of the response data
        """
        self._led1_pattern = int(data[0])
        self._led2_pattern = int(data[1])
        self._led3_pattern = int(data[2])
        self._led4_pattern = int(data[3])
        self._led5_pattern = int(data[4])
        self._buzzer_pattern = int(data[5])

    @property
    def led1_pattern(self) -> int:
        """1st LED unit pattern"""
        return self._led1_pattern

    @property
    def led2_pattern(self) -> int:
        """2nd LED unit pattern"""
        return self._led2_pattern

    @property
    def led3_pattern(self) -> int:
        """3rd LED unit pattern"""
        return self._led3_pattern

    @property
    def led4_pattern(self) -> int:
        """4th LED unit pattern"""
        return self._led4_pattern

    @property
    def led5_pattern(self) -> int:
        """5th LED unit pattern"""
        return self._led5_pattern

    @property
    def buzzer_pattern(self) -> int:
        """buzzer patterns 1 through 11"""
        return self._buzzer_pattern

    def __str__(self):
        return "LedModeStateData(led1_pattern={}, led2_pattern={}, led3_pattern={}, led4_pattern={}, led5_pattern={}, buzzer_pattern={})".format(
            self._led1_pattern,
            self._led2_pattern,
            self._led3_pattern,
            self._led4_pattern,
            self._led5_pattern,
            self._buzzer_pattern,
        )


class SmartModeStateData(PNSStateData):
    """state data when running smart mode"""

    def __init__(self, data: bytes):
        """
        state data when running smart mode

        Parameters
        ----------
        data: bytes
            Smart mode" portion of response data
        """
        self._group_no = int(data[0])
        self._mute = int(data[1])
        self._stop_input = int(data[2])
        self._pattern_no = int(data[3])

    @property
    def group_no(self) -> int:
        """group number"""
        return self._group_no

    @property
    def mute(self) -> int:
        """mute"""
        return self._mute

    @property
    def stop_input(self) -> int:
        """STOP input"""
        return self._stop_input

    @property
    def pattern_no(self) -> int:
        """pattern number"""
        return self._pattern_no

    def __str__(self):
        return "SmartModeStateData(group_no={}, mute={}, stop_input={}, pattern_no={})".format(
            self._group_no, self._mute, self._stop_input, self._pattern_no
        )


class LEDModeDetailStateData(PNSStateData):
    """detailed state data when running in signal light mode"""

    def __init__(self, data: bytes):
        """
        detailed state data when running in signal light mode

        Parameters
        ----------
        data: bytes
            LED unit 1st stage" to "buzzer patterns" part of response data
        """
        self._led_unit1_data = LEDUnitData(data[0:4])
        self._led_unit2_data = LEDUnitData(data[4:8])
        self._led_unit3_data = LEDUnitData(data[8:12])
        self._led_unit4_data = LEDUnitData(data[12:16])
        self._led_unit5_data = LEDUnitData(data[16:20])
        self._buzzer_pattern = int(data[20])

    @property
    def led_unit1_data(self) -> "LEDUnitData":
        """1st stage of LED unit"""
        return self._led_unit1_data

    @property
    def led_unit2_data(self) -> "LEDUnitData":
        """2nd stage of LED unit"""
        return self._led_unit2_data

    @property
    def led_unit3_data(self) -> "LEDUnitData":
        """3rd stage of LED unit"""
        return self._led_unit3_data

    @property
    def led_unit4_data(self) -> "LEDUnitData":
        """4th stage of LED unit"""
        return self._led_unit4_data

    @property
    def led_unit5_data(self) -> "LEDUnitData":
        """5th stage of LED unit"""
        return self._led_unit5_data

    @property
    def buzzer_pattern(self) -> int:
        """buzzer pattern 1 to 11"""
        return self._buzzer_pattern

    def __str__(self) -> str:
        return "LEDModeDetailData(led_unit1_data={}, led_unit2_data={}, led_unit3_data={}, led_unit4_data={}, led_unit5_data={}, buzzer_pattern={})".format(
            self._led_unit1_data,
            self._led_unit2_data,
            self._led_unit3_data,
            self._led_unit4_data,
            self._led_unit5_data,
            self._buzzer_pattern,
        )


class LEDUnitData(PNSStateData):
    """LED unit data"""

    def __init__(self, data: bytes):
        """
        LED unit data

        Parameters
        ----------
        data: bytes
            LED unit X" part of the response data
        """
        self._led_pattern = int(data[0])
        self._red = int(data[1])
        self._green = int(data[2])
        self._blue = int(data[3])

    @property
    def led_pattern(self) -> int:
        """status"""
        return self._led_pattern

    @property
    def red(self) -> int:
        """R"""
        return self._red

    @property
    def green(self) -> int:
        """G"""
        return self._green

    @property
    def blue(self) -> int:
        """B"""
        return self._blue

    def __str__(self) -> str:
        return "LEDUnitData(led_pattern={}, red={}, green={}, blue={})".format(
            self._led_pattern, self._red, self._green, self._blue
        )


class SmartModeDetailStateData(PNSStateData):
    """detail state data for smart mode execution"""

    def __init__(self, data: bytes):
        """
        detail state data for smart mode execution

        Parameters
        ----------
        data: bytes
             Smart mode status" to "Buzzer patterns" portion of response data
        """
        self._smart_mode_data = SmartModeDetailStateData(data[0:5])
        self._led_unit1_data = LEDUnitData(data[5:9])
        self._led_unit2_data = LEDUnitData(data[9:13])
        self._led_unit3_data = LEDUnitData(data[13:17])
        self._led_unit4_data = LEDUnitData(data[17:21])
        self._led_unit5_data = LEDUnitData(data[21:25])
        self._buzzer_pattern = BUZZER_CONTROL(data[25])

    @property
    def smart_mode_data(self) -> "SmartModeDetailStateData":
        """smart mode state"""
        return self._smart_mode_data

    @property
    def led_unit1_data(self) -> "LEDUnitData":
        """1st stage of LED unit"""
        return self._led_unit1_data

    @property
    def led_unit2_data(self) -> "LEDUnitData":
        """2nd stage of LED unit"""
        return self._led_unit2_data

    @property
    def led_unit3_data(self) -> "LEDUnitData":
        """3rd stage of LED unit"""
        return self._led_unit3_data

    @property
    def led_unit4_data(self) -> "LEDUnitData":
        """4th stage of LED unit"""
        return self._led_unit4_data

    @property
    def led_unit5_data(self) -> "LEDUnitData":
        """5th stage of LED unit"""
        return self._led_unit5_data

    @property
    def buzzer_pattern(self) -> int:
        """buzzer pattern 1 to 11"""
        return self._buzzer_pattern

    def __str__(self) -> str:
        return "SmartModeDetailData(smart_mode_data={}, led_unit1_data={}, led_unit2_data={}, led_unit3_data={}, led_unit4_data={}, led_unit5_data={}, buzzer_pattern={})".format(
            self._smart_mode_data,
            self._led_unit1_data,
            self._led_unit2_data,
            self._led_unit3_data,
            self._led_unit4_data,
            self._led_unit5_data,
            self._buzzer_pattern,
        )


class SmartModeDetailStateData(PNSStateData):
    """smart mode status data"""

    def __init__(self, data: bytes):
        """
        smart mode status data

        Parameters
        ----------
        data: bytes
            Smart mode status" portion of response data
        """
        self._group_no = int(data[0])
        self._mute = int(data[1])
        self._stop_input = int(data[2])
        self._pattern_no = int(data[3])
        self._last_pattern = int(data[4])

    @property
    def group_no(self) -> int:
        """group number"""
        return self._group_no

    @property
    def mute(self) -> int:
        """mute"""
        return self._mute

    @property
    def stop_input(self) -> int:
        """STOP input"""
        return self._stop_input

    @property
    def pattern_no(self) -> int:
        """pattern number"""
        return self._pattern_no

    @property
    def last_pattern(self) -> int:
        """last pattern"""
        return self._last_pattern

    def __str__(self) -> str:
        return "SmartModeDetailStateData(group_no={}, mute={}, stop_input={}, pattern_no={}, last_pattern={})".format(
            self._group_no, self._mute, self._stop_input, self._pattern_no, self._last_pattern
        )
