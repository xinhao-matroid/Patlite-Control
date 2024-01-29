import socket

from .actions import PatliteRequest, PatliteResponse


class PatliteControl:
    def __init__(self, ip: str, port: int) -> None:
        try:
            socket.inet_aton(ip)
        except Exception as e:
            raise RuntimeError("Invalid IPv4 address. Only IPv4 addresses are supported.") from e
        self.ip = ip
        self.port = port
        if port < 0 or port > 65535:
            raise RuntimeError("Port must with in range")
        self._sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self._sock.connect((self.ip, self.port))

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._sock.close()

    def send_data(self, send_data: bytes) -> bytes:
        # Send
        self._sock.send(send_data)

        # Receive response data
        recv_data = self._sock.recv(1024)

        return recv_data

    def send_request(self, request: PatliteRequest) -> PatliteResponse:
        return request.send(self.send_data)
