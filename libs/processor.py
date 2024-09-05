# -*- coding: utf-8 -*-
"""
  processor.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 2.09.2024, 15:50:03
  
  Purpose: 
"""

import time, os

from typing import Optional, List
from threading import Event, Thread
from queue import Queue, Empty

from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue
from jsktoolbox.libs.base_th import ThBaseObject
from jsktoolbox.libs.system import PathChecker

from libs.base import BDebug, BDir, BMiles, BVerbose, BLogs, BStop
from libs.model import MotoStat, SpritMonitor


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    QUEUE: str = "__comms_queue__"


class CsvProcessor(Thread, ThBaseObject, BLogs, BStop, BMiles, BVerbose, BDebug, BDir):
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

        # check output dir
        out_dir = PathChecker(f"{self.output_dir}/")
        if out_dir.exists and out_dir.is_dir:
            pass
        else:
            if not out_dir.exists:
                if not out_dir.create():
                    self.logs.message_error = (
                        f"Cannot create output directory: '{self.output_dir}', exiting."
                    )
                    return
            if out_dir.is_file:
                self.logs.message_error = (
                    f"Output dir: '{self.output_dir}' existing and is a file, exiting."
                )
                return

        # data
        data: List[MotoStat] = []
        sprit_fuels: List[SpritMonitor] = []
        sprit_costs: List[SpritMonitor] = []

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
            for item in sorted(data, reverse=True):
                if item.cost_id:
                    sprit_costs.append(SpritMonitor(item))
                if item.fuel_id:
                    sprit_fuels.append(SpritMonitor(item))
            self.__write_costs(sprit_costs)
            self.__write_fuels(sprit_fuels)

        # exit
        if self.debug:
            self.logs.message_debug = "stopped."

    def __write_costs(self, data: List[SpritMonitor]) -> None:
        """Write csv."""
        csv_path: str = os.path.join(self.output_dir, "spritmonitor_costs.csv")
        if data:
            with open(csv_path, "w") as file:
                file.write(f"{data[0].csv_header}\n")
                for item in data:
                    file.write(f"{item.csv_data}\n")

    def __write_fuels(self, data: List[SpritMonitor]) -> None:
        """Write csv."""
        csv_path: str = os.path.join(self.output_dir, "spritmonitor_fuels.csv")
        if data:
            with open(csv_path, "w") as file:
                file.write(f"{data[0].csv_header}\n")
                for item in data:
                    file.write(f"{item.csv_data}\n")

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
