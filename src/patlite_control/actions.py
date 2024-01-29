import struct
from .constants import PNS, PHNCONTROL
from abc import ABC, abstractmethod
from .messages import *
from typing import Callable

PNS_PRODUCT_ID = PNS.PRODUCT_ID


# Abstract Request
class PatliteRequest(ABC):
    def __init__(self, payload: PatliteData) -> None:
        self.payload = payload

    @property
    @abstractmethod
    def command_identifier(self) -> bytes:
        pass

    @property
    @abstractmethod
    def data_format(self) -> bytes:
        pass

    @abstractmethod
    def send(self, send: Callable[[bytes], "PatliteResponse"]) -> "PatliteResponse":
        pass


class PatlitePNSRequest(PatliteRequest):
    data_format = ">2ssxH"  # default format

    def pack(self) -> bytes:
        return (
            struct.pack(
                self.data_format,  # format
                PNS_PRODUCT_ID,  # Product Category (AB), single one for now
                self.command_identifier,  # Command identifier (T)
                self.payload.data_size(),  # Data size
            )
            + self.payload.pack()
        )

    def send(self, send) -> "PatlitePNSResponse":
        return PatlitePNSResponse(send(self.pack()))


class PatlitePHNRequest(PatliteRequest):
    def pack(self):
        return struct.pack(self.data_format, self.command_identifier)

    def send(self, send) -> "PatlitePHNResponse":
        return PatlitePHNResponse(send(self.pack()))


# Abstract Response
class PatliteResponse(ABC):
    def __init__(self, data) -> None:
        self.data = data

    @property
    @abstractmethod
    def cmd_ack(self) -> bytes:
        pass

    @property
    @abstractmethod
    def cmd_nak(self) -> bytes:
        pass

    def is_bad_response(self) -> bool:
        return self.data[0] == self.cmd_nak

    def __str__(self) -> str:
        return f"Response: {self.data}"


class PatlitePNSResponse(PatliteResponse):
    cmd_ack = 0x06
    cmd_nak = 0x15


class PatlitePHNResponse(PatliteResponse):
    cmd_ack = b"ACK"
    cmd_nak = b"NAK"


class ReadCommandResponse(PatlitePHNResponse):
    """
    Returns
    -------
    data: int
        Received data of read command (operation data of LED unit 1 to 3 stages lighting and blinking, buzzer pattern 1,2)
    """

    PHN_READ_COMMAND = b"R"

    def is_bad_response(self):
        return self.data[0] != int(self.PHN_READ_COMMAND.hex(), 16)

    def __str__(self) -> str:
        return f"""LED unit flashing:
1st LED unit : {self.data & PHNCONTROL.LED_UNIT1_BLINKING}
2nd LED unit : {self.data & PHNCONTROL.LED_UNIT2_BLINKING}
3rd LED unit : {self.data & PHNCONTROL.LED_UNIT3_BLINKING}
buzzer pattern:
pattern1 : {self.data & PHNCONTROL.BUZZER_PATTERN1}
pattern2 : {self.data & PHNCONTROL.BUZZER_PATTERN2}
LED unit lighting:
1st LED unit : {self.data & PHNCONTROL.LED_UNIT1_LIGHTING}
2nd LED unit : {self.data & PHNCONTROL.LED_UNIT2_LIGHTING}
3rd LED unit : {self.data & PHNCONTROL.LED_UNIT3_LIGHTING}
"""


### Begin Requests
class SmartModeCommandRequest(PatlitePNSRequest):
    """
    Send smart mode control command for PNS command

    Smart mode can be executed for the number specified in the data area
    """

    command_identifier = b"T"

    def __init__(self, payload: SmartModeCommandData) -> None:
        super().__init__(payload)


class MuteCommandRequest(PatlitePNSRequest):
    """
    Send mute command for PNS command

    Can control the buzzer ON/OFF while Smart Mode is running
    """

    command_identifier = b"M"

    def __init__(self, payload: MuteCommandData) -> None:
        super().__init__(payload)


class StopPulseInputCommand(PatlitePNSRequest):
    """
    Send stop/pulse input command for PNS command

    Transmit during time trigger mode operation to control stop/resume of pattern (STOP input)

    Sending this command during pulse trigger mode operation enables pattern transition (trigger input)
    """

    command_identifier = b"P"

    def __init__(self, payload: StopPulseInputCommandData) -> None:
        super().__init__(payload)


class RunControlCommandRequest(PatlitePNSRequest):
    """
    Send operation control command for PNS command

    Each stage of the LED unit and the buzzer (1 to 3) can be controlled by the pattern specified in the data area

    Operates with the color and buzzer set in the signal light mode
    """

    command_identifier = b"S"

    def __init__(self, payload: RunControlCommandData) -> None:
        super().__init__(payload)


class DetailRunControlCommandRequest(PatlitePNSRequest):
    """
    Send detailed operation control command for PNS command

    The color and operation pattern of each stage of the LED unit and the buzzer pattern (1 to 11) can be specified and controlled in the data area
    """

    command_identifier = b"D"

    def __init__(self, payload: DetailRunControlCommandData) -> None:
        super().__init__(payload)


class ClearCommandRequest(PatlitePNSRequest):
    """
    Send clear command for PNS command

    Turn off the LED unit and stop the buzzer
    """

    command_identifier = b"C"

    def __init__(self) -> None:
        super().__init__(EmptyData())


class RebootCommandRequest(PatlitePNSRequest):
    """
    Send restart command for PNS command

    LA6-POE can be restarted
    """

    command_identifier = b"B"

    def __init__(self, password: str) -> None:
        super().__init__(PasswordCommandData(password))


class GetDataCommandRequest(PatlitePNSRequest):
    """
    Send status acquisition command for PNS command

    Signal line/contact input status and LED unit and buzzer status can be acquired
    """

    command_identifier = b"G"

    def __init__(self) -> None:
        super().__init__(EmptyData())

    def send(self, send) -> "StatusResponseData":
        return StatusResponseData(send(self.pack()))


class GetDetailDataCommandRequest(PatlitePNSRequest):
    """
    Send command to get detailed status of PNS command

    Signal line/contact input status, LED unit and buzzer status, and color information for each stage can be acquired
    """

    command_identifier = b"E"

    def __init__(self) -> None:
        super().__init__(EmptyData())

    def send(self, send) -> "DetailStatusResponseData":
        return DetailStatusResponseData(send(self.pack()))


class WriteCommandRequest(PatlitePHNRequest):
    """
    Send write command for PNS command

    Can control the lighting and blinking of LED units 1 to 3 stages, and buzzer patterns 1 and 2
    """

    command_identifier = b"W"
    data_format = "sB"

    def __init__(self, payload: GeneralData) -> None:
        super().__init__(payload)

    def pack(self) -> bytes:
        return struct.pack(self.data_format, self.command_identifier, self.payload.pack())


class ReadCommandRequest(PatlitePHNRequest):
    """
    Send command to read PHN command

    Get information about LED unit 1 to 3 stage lighting and blinking, and buzzer pattern 1 and 2
    """

    command_identifier = b"R"
    data_format = "s"

    def __init__(self) -> None:
        super().__init__(EmptyData())

    def pack(self):
        return struct.pack(self.data_format, self.command_identifier)

    def send(self, send) -> "ReadCommandResponse":
        return ReadCommandResponse(send(self.pack()))
