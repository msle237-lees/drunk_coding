#!/usr/bin/env python3

from io import BytesIO
import logging
import socket
from typing import Any

import numpy as np


class NP(socket.socket):
    def sendall(self, frame: np.ndarray) -> None:  # type: ignore[override]
        out = self.__pack_frame(frame)
        super().sendall(out)
        logging.debug("frame sent")

    def send_string_as_bytes(self, string: str) -> None:
        byte_array = string.encode('utf-8')
        super().sendall(byte_array)
        logging.debug(f"String '{string}' sent as bytes")

    def recv(self, bufsize: int = 1024) -> np.ndarray:  # type: ignore[override]
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
                    length_str, ignored, frame_buffer = frame_buffer.partition(b":")
                    length = int(length_str)

                if len(frame_buffer) < length:
                    break

                frame_data = frame_buffer[:length]
                frame_buffer = frame_buffer[length:]
                frame = np.load(BytesIO(frame_data), allow_pickle=True)["frame"]
                logging.debug("frame received")
                return frame

    def accept(self) -> tuple["NP", tuple[str, int] | tuple[Any, ...]]:
        fd, addr = super()._accept()  # type: ignore
        sock = NP(super().family, super().type, super().proto, fileno=fd)

        if socket.getdefaulttimeout() is None and super().gettimeout():
            sock.setblocking(True)
        return sock, addr

    @staticmethod
    def __pack_frame(frame: np.ndarray) -> bytearray:
        f = BytesIO()
        np.savez(f, frame=frame)

        packet_size = len(f.getvalue())
        header = "{0}:".format(packet_size)
        header_bytes = bytes(header.encode())  # prepend length of array

        out = bytearray()
        out += header_bytes
        f.seek(0)
        out += f.read()

        return out

