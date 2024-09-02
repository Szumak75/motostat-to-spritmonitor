# -*- coding: utf-8 -*-
"""
  model.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 2.09.2024, 15:50:29
  
  Purpose: 
"""

import re

from typing import Any, Iterable, Mapping, Optional, List, Tuple, Dict
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


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal keys class."""

    DATA: str = "__data__"


class MotoStat(BDebug, BVerbose):
    """MotoStat data class."""

    def __init__(self, csv_line: str) -> None:
        """Constructor."""
        data_dict: Dict[str, Any] = {}
        csv_header: List[str] = [
            "cost_id",
            "fueling_id",
            "cost_type",
            "date",
            "fuel_id",
            "gas_station_id",
            "odometer",
            "trip_odometer",
            "quantity",
            "cost",
            "notes",
            "fueling_type",
            "tires",
            "driving_style",
            "route_motorway",
            "route_country",
            "route_city",
            "bc_consumption",
            "bc_avg_speed",
            "ac",
            "currency",
            "fuel_name",
            "gas_station_name",
        ]
        data = re.split(""";(?=(?:[^"]|'[^']*'|"[^"]*")*$)""", csv_line)
        if len(data) == len(csv_header):
            if data[0] != csv_header[0]:
                for i in range(0, len(data)):
                    data_dict[csv_header[i]] = data[i]
        self._set_data(key=_Keys.DATA, value=data_dict, set_default_type=Dict)
        self.__time_update()

    def __repr__(self) -> str:
        tmp = ""
        for i, v in self._get_data(key=_Keys.DATA).items():  # type: ignore
            tmp += f"'{i}':{v},"
        return f"{self._c_name}({tmp})"

    def __time_update(self) -> None:
        """Generate timestamp from date and id."""
        if not self.is_empty:
            cost_id: str = self._get_data(key=_Keys.DATA)["cost_id"]  # type: ignore
            fueling_id: str = self._get_data(key=_Keys.DATA)["fueling_id"]  # type: ignore
            date: str = self._get_data(key=_Keys.DATA)["date"]  # type: ignore
            ts = Timestamp.from_string(date, "%Y-%m-%d")
            ms: float = 0.0
            if len(cost_id) > 0:
                ms = float(f"{ts}.{cost_id}")
            else:
                ms = float(f"{ts}.{fueling_id}")
            print(f"{cost_id}::{fueling_id}::{date}:::{ts}:::{ms}")

    @property
    def is_empty(self) -> bool:
        """Returns True if data is empty."""
        return len(self._get_data(key=_Keys.DATA, default_value={})) == 0  # type: ignore


# #[EOF]#######################################################################
