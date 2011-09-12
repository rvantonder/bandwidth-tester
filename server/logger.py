import logging
import os

class Logger:
  def __init__(self, logfilename):
    os.remove(logfilename)

    self.logger = logging.getLogger("logger")
    self.hdlr = logging.FileHandler(logfilename)
    self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s %(message)s')
    self.hdlr.setFormatter(self.formatter)
    self.logger.addHandler(self.hdlr)
    self.logger.setLevel(logging.INFO)
