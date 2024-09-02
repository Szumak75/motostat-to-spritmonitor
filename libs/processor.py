# -*- coding: utf-8 -*-
"""
  processor.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 2.09.2024, 15:50:03
  
  Purpose: 
"""

import time

from collections.abc import Callable
from typing import Any, Iterable, Mapping, Optional, List, Tuple
from threading import Event, Thread
from inspect import currentframe
from queue import Queue, Empty

from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue
from jsktoolbox.libs.base_th import ThBaseObject
from jsktoolbox.netaddresstool.ipv4 import Address, Network
from jsktoolbox.raisetool import Raise
from jsktoolbox.devices.network.connectors import API
from jsktoolbox.devices.mikrotik.routerboard import RouterBoard
from jsktoolbox.datetool import Timestamp

from libs.base import BDebug, BVerbose, BLogs, BStop
from libs.model import MotoStat


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    QUEUE: str = "__comms_queue__"


class CsvProcessor(Thread, ThBaseObject, BLogs, BStop, BVerbose, BDebug):
    """Csv data processor class."""

    def __init__(
        self,
        logger_queue: LoggerQueue,
        comms_queue: Queue,
        verbose: bool = False,
        debug: bool = False,
    ) -> None:
        """Constructor.

        ### Arguments:
        - logger_queue [LoggerQueue] - logger queue for communication.
        - comms_queue [Queue] - communication queue.
        - debug [bool] - debug flag.
        - verbose [bool] - verbose flag.
        """
        # init thread
        Thread.__init__(self, name=f"{self._c_name}")
        self._stop_event = Event()
        self.sleep_period = 0.2
        # debug
        self.debug = debug
        # verbose
        self.verbose = verbose
        # logger
        self.logs = LoggerClient(logger_queue, f"{self._c_name}")
        # communication queue
        self.__comms_queue = comms_queue

    def run(self) -> None:
        """Start processor."""
        if not self._stop_event:
            return None
        if not self.__comms_queue:
            self.logs.message_critical = f"Communication queue was not set properly."
            return None

        # main loop
        while True:
            if self.__comms_queue.empty() and self._stop_event.is_set():
                break
            try:
                # getting data from queue
                line: str = self.__comms_queue.get(block=False)
                item = MotoStat(line.strip())
                if not item.is_empty:
                    print(item)
            except Empty:
                time.sleep(0.1)

        # exit
        if self.debug:
            self.logs.message_debug = "stopped."

    def stop(self) -> None:
        """Sets stop event."""
        if self._stop_event:
            if self.debug:
                self.logs.message_debug = "stopping..."
            self._stop_event.set()

    @property
    def __comms_queue(self) -> Optional[Queue]:
        """Returns communication queue if set."""
        return self._get_data(key=_Keys.QUEUE, set_default_type=Optional[Queue])

    @__comms_queue.setter
    def __comms_queue(self, comms_queue: Optional[Queue]) -> None:
        """Sets communication queue."""
        self._set_data(key=_Keys.QUEUE, value=comms_queue)


# #[EOF]#######################################################################
