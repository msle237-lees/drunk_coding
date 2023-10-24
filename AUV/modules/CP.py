import cv2
from modules.NP import NP
import logging
from multiprocessing import Pipe


class CP:
    def __init__(self, sim : bool = False, pipe : Pipe = None):
        self.sim_toggle = sim

        if self.sim_toggle:
            self.setup_sim()
        else:
            self.setup()

        self.comm_pipe = pipe

    

    