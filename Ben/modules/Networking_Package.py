#!/usr/bin/env python3

from io import BytesIO
import logging
import socket
from typing import Any  # Python 3.6 supports this basic typing

import numpy as np

class NP(socket.socket):
    """
    NP class documentation.
    """

    def sendall(self, frame: np.ndarray) -> None:
        """
        sendall method documentation.
        """
        out = self.__pack_frame(frame)
        super_socket = super()
        super_socket.sendall(out)
        logging.debug("frame sent")

    def send_string_as_bytes(self, string: str) -> None:
        """
        send_string_as_bytes method documentation.
        """
        byte_array = string.encode('utf-8')
        super().sendall(byte_array)
        logging.debug("String '{}' sent as bytes".format(string))

    def recv(self, bufsize: int = 1024) -> np.ndarray:
        """
        recv method documentation.
        """
        length = None
        frame_buffer = bytearray()
        while True:
            data = super().recv(bufsize)
            if len(data) == 0:
                return np.array([])
            frame_buffer += data

            while True:
                if length is None:
                    if b":" not in frame_buffer:
                        break
                    length_str, _, frame_buffer = frame_buffer.partition(b":")
                    length = int(length_str)

                if len(frame_buffer) < length:
                    break

                frame_data = frame_buffer[:length]
                frame_buffer = frame_buffer[length:]
                frame = np.load(BytesIO(frame_data), allow_pickle=True)["frame"]
                logging.debug("frame received")
                return frame

    def recv_string_as_bytes(self, bufsize: int = 1024) -> str:
        """
        recv_string_as_bytes method documentation.
        """
        data = super().recv(bufsize)
        if len(data) == 0:
            return ""
        decoded_string = data.decode('utf-8')
        logging.debug("Received string as bytes: {}".format(decoded_string))
        return decoded_string

    def accept(self) -> tuple['NP', tuple[str, int] | tuple[Any, ...]]:
        """
        accept method documentation.
        """
        super_socket = super()
        fd, addr = super_socket._accept()
        sock = NP(super_socket.family, super_socket.type, super_socket.proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super_socket.gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_frame(frame: np.ndarray) -> bytearray:
        """
        __pack_frame static method documentation.
        """
        f = BytesIO()
        np.savez(f, frame=frame)

        packet_size = len(f.getvalue())
        header = "{}:".format(packet_size)
        header_bytes = bytes(header.encode())

        out = bytearray(header_bytes)
        f.seek(0)
        out += f.read()

        return out
