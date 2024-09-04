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

from libs.base import BDebug, BMiles, BVerbose, BLogs, BStop
from libs.model import MotoStat, SpritMonitor


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    QUEUE: str = "__comms_queue__"


class CsvProcessor(Thread, ThBaseObject, BLogs, BStop, BMiles, BVerbose, BDebug):
    """Csv data processor class."""

    def __init__(
        self,
        logger_queue: LoggerQueue,
        comms_queue: Queue,
        miles: bool = False,
        verbose: bool = False,
        debug: bool = False,
    ) -> None:
        """Constructor.

        ### Arguments:
        - logger_queue [LoggerQueue] - logger queue for communication.
        - comms_queue [Queue] - communication queue.
        - miles [bool] - mileage in miles flag.
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
        # miles
        self.miles = miles
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

        # data
        data: List[MotoStat] = []
        sprit: List[SpritMonitor] = []

        # main loop
        while True:
            if self.__comms_queue.empty() and self._stop_event.is_set():
                break
            try:
                # getting data from queue
                line: str = self.__comms_queue.get(block=False)
                item = MotoStat(csv_line=line.strip(), miles=self.miles)
                if not item.is_empty:
                    data.append(item)
            except Empty:
                time.sleep(0.1)

        # processing data
        if data:
            # last: float = 0
            # trip: float = 0
            # last_gas: float = 0
            # trip_gas: float = 0
            # self.logs.message_info = f"Found: {len(data)} records."
            # # print(sorted(data))
            # for item in sorted(data):
            #     if item.gas:
            #         if last_gas > 0:
            #             trip_gas = float(item.odometer) - last_gas
            #         last_gas = float(item.odometer)
            #     else:
            #         if last > 0:
            #             trip = float(item.odometer) - last
            #         last = float(item.odometer)
            #     if item.gas:
            #         print(
            #             f"{item.date}: {item.cost_id}{item.fueling_id}: odometer: {item.odometer}, {item.trip_odometer} - calc: {trip_gas}"
            #         )
            #     else:
            #         print(
            #             f"{item.date}: {item.cost_id}{item.fueling_id}: odometer: {item.odometer}, {item.trip_odometer} - calc: {trip}"
            #         )
            for item in sorted(data):
                sprit.append(SpritMonitor(item))
                # print(f"{SpritMonitor(item)}")

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
