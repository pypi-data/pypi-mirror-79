import logging
import socket
import threading
import time
from queue import Queue

import numpy as np

from third_party.rtde import rtde
from urinterface.recording import _recording_thread, STOP_REQUEST

_log = logging.getLogger("RobotConnection")

class RobotConnection:
    # ip_adr: <string>
    # controller_socket, dashboard_socket: <socket>
    # is_logging_data: <bool>

    def __init__(self, ip_adr,
                 controller_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                 dashboard_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        self.ip_adr = ip_adr
        self.recording_thread = None
        self.recording_thread_queue = Queue()
        self.logging_process = None
        controller_port = 30002
        dashboard_port = 29999

        self.buff_size = 1024

        # Create and connect to controller and dashboard TCP/IP sockets
        self.controller_socket = controller_socket
        self.dashboard_socket = dashboard_socket
        self.dashboard_socket.connect((ip_adr, dashboard_port))
        self.controller_socket.connect((ip_adr, controller_port))

        reply = self._receive_ascii_bytes(self.dashboard_socket)
        assert reply.startswith("Connected")

    def _receive_ascii_bytes(self, socket):
        reply = socket.recv(self.buff_size)
        _log.info(f"receiving bytes:{reply}")
        reply_ascii = reply.decode(encoding="ascii")
        _log.info(f"receiving:{reply_ascii}")
        return reply_ascii

    def _send_ascii_bytes(self, msg, socket):
        to_send = bytes(msg, encoding="ASCII")
        _log.info(f"sending:{to_send}")
        socket.sendall(to_send)
        _log.info("sent.")

    def __del__(self):
        # Should it stop recording here???
        # TODO : When deleting the object, make sure that only connected sockets will be closed.
        self.dashboard_socket.shutdown(socket.SHUT_RDWR)
        self.controller_socket.shutdown(socket.SHUT_RDWR)
        self.dashboard_socket.close()
        self.controller_socket.close()

    def _ensure_ready(self):
        reply = "Program running: true"
        while not reply.startswith("Program running: false"):
            time.sleep(0.12)  # seconds
            self._send_ascii_bytes("running\n", self.dashboard_socket)
            reply = self._receive_ascii_bytes(self.dashboard_socket)
        assert reply.startswith("Program running: false"), reply

    def movej(self, q=np.zeros(6), v=None, a=None, t=None, r=None):
        # ensure that the robot is in the remote control mode
        self._ensure_ready()
        q_string = np.array2string(q, precision=6, separator=',').replace(" ", "")
        opts = []
        if a is not None:
            opts.append(f"a={a}")
        if v is not None:
            opts.append(f"v={v}")
        if t is not None:
            opts.append(f"t={t}")
        if r is not None:
            opts.append(f"r={r}")

        opts_string = ", ".join(opts)
        if len(opts) > 0:
            opts_string = ", " + opts_string

        program = "movej("+q_string+opts_string+")\n"
        self._send_ascii_bytes(program, self.controller_socket)
        self._ensure_ready()

    def stop_motion(self):
        self._send_ascii_bytes("stop\n", self.dashboard_socket)
        return self.dashboard_socket.recv(1024).decode() == "Stopped"

    def record_samples(self, config_file='resources/record_configuration.xml', filename='robotdata.csv', frequency=500, samples=10, rtde_port=30004, RtdeConstructor=rtde.RTDE):
        assert samples>0, "Expected positive number of samples. Use start_recording for samples=0."
        self.start_recording(config_file, filename, frequency, samples, rtde_port, RtdeConstructor)
        self.stop_recording()

    def start_recording(self, config_file='resources/record_configuration.xml', filename='robotdata.csv', frequency=500, samples=0, rtde_port=30004, RtdeConstructor=rtde.RTDE):
        # TODO Check that the filename does not exist and give error in case it does.
        assert self.recording_thread is None, "Already logging."

        connection = RtdeConstructor(self.ip_adr, rtde_port)

        self.recording_thread = threading.Thread(target=_recording_thread,
                                                 args=
                                                 [
                                                     connection,
                                                     config_file,
                                                     filename,
                                                     frequency,
                                                     samples,
                                                     self.recording_thread_queue
                                                 ]
                                                 )
        self.recording_thread.start()

    def stop_recording(self):
        assert self.recording_thread is not None, "Should be recording data."

        _log.debug(f"Stop recording requested.")

        assert self.recording_thread_queue.empty(), "Expected this queue to be empty"
        self.recording_thread_queue.put(STOP_REQUEST)

        _log.debug(f"Waiting for thread to finish.")
        self.recording_thread.join()
        _log.debug(f"Thread finished.")
        self.recording_thread = None

        _stop_recording = False