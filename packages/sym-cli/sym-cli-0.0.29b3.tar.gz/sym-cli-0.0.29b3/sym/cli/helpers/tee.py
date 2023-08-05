import os
import sys
from pathlib import Path
from typing import Literal

# http://web.archive.org/web/20141016185743/https://mail.python.org/pipermail/python-list/2007-May/460639.html

TeeFD = Literal["stdout", "stderr"]


class Tee(object):
    def __init__(self, fd_name: TeeFD, log_dir: str, mode="w"):
        path = Path(log_dir) / f"{os.getpid()}.{fd_name}.log"
        path.parent.mkdir(parents=True, exist_ok=True)

        self.file = path.open(mode)
        self.fd_name = fd_name
        self.fd = getattr(sys, fd_name)
        setattr(sys, fd_name, self)

    def close(self):
        if self.fd is not None:
            setattr(sys, self.fd_name, self.fd)
            self.fd = None

        if self.file is not None:
            self.file.close()
            self.file = None

    def write(self, data):
        self.file.write(data)
        self.fd.write(data)

    def flush(self):
        self.file.flush()
        self.fd.flush()

    def __enter__(self):
        self.ref = self

    def __exit__(self, type, value, traceback):
        self.ref = None
        self.close()

    def __del__(self):
        self.close()


class TeeStdOut(Tee):
    def __init__(self, log_dir):
        super().__init__("stdout", log_dir)


class TeeStdErr(Tee):
    def __init__(self, log_dir):
        super().__init__("stderr", log_dir)
