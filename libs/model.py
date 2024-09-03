# -*- coding: utf-8 -*-
"""
  model.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 2.09.2024, 15:50:29
  
  Purpose: 
"""

import re

from typing import Any, Iterable, Mapping, Optional, List, Tuple, Dict, TypeVar, Union
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

TMotoStat = TypeVar("TMotoStat", bound="MotoStat")


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
        # print(csv_line)
        if len(data) == len(csv_header) - 2:
            data.append("")
            data.append("")
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
            data = self._get_data(key=_Keys.DATA)
            cost_id: str = data["cost_id"]  # type: ignore
            fueling_id: str = data["fueling_id"]  # type: ignore
            date: str = data["date"]  # type: ignore
            ts = Timestamp.from_string(date, "%Y-%m-%d")
            ms: float = 0.0
            if len(cost_id) > 0:
                ms = ts + float(f"{cost_id}") / 10000
            else:
                ms = ts + float(f"{fueling_id}") / 10000
            data["date"] = ms  # type: ignore
            # print(f"{cost_id}::{fueling_id}::{date}:::{ts}:::{ms}")

    @property
    def is_empty(self) -> bool:
        """Returns True if data is empty."""
        return len(self._get_data(key=_Keys.DATA, default_value={})) == 0  # type: ignore

    # "cost_id",
    @property
    def cost_id(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["cost_id"]  # type: ignore
            return out
        else:
            return ""

    # "fueling_id",
    @property
    def fueling_id(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["fueling_id"]  # type: ignore
            return out
        else:
            return ""

    # "cost_type",
    @property
    def cost_type(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["cost_type"]  # type: ignore
            return out
        else:
            return ""

    # "date",
    @property
    def date(self) -> float:
        if self._get_data(key=_Keys.DATA, default_value={}):
            date: float = self._get_data(key=_Keys.DATA)["date"]  # type: ignore
            return date
        else:
            return 0.0

    # "fuel_id",
    @property
    def fuel_id(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["fuel_id"]  # type: ignore
            return out
        else:
            return ""

    # "gas_station_id",
    @property
    def gas_station_id(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["gas_station_id"]  # type: ignore
            return out
        else:
            return ""

    # "odometer",
    @property
    def odometer(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["odometer"]  # type: ignore
            return out
        else:
            return ""

    # "trip_odometer",
    @property
    def trip_odometer(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["trip_odometer"]  # type: ignore
            return out
        else:
            return ""

    # "quantity",
    @property
    def quantity(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["quantity"]  # type: ignore
            return out
        else:
            return ""

    # "cost",
    @property
    def cost(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["cost"]  # type: ignore
            return out
        else:
            return ""

    # "notes",
    @property
    def notes(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["notes"]  # type: ignore
            return out
        else:
            return ""

    # "fueling_type",
    @property
    def fueling_type(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["fueling_type"]  # type: ignore
            return out
        else:
            return ""

    # "tires",
    @property
    def tires(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["tires"]  # type: ignore
            return out
        else:
            return ""

    # "driving_style",
    @property
    def driving_style(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["driving_style"]  # type: ignore
            return out
        else:
            return ""

    # "route_motorway",
    @property
    def route_motorway(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["route_motorway"]  # type: ignore
            return out
        else:
            return ""

    # "route_country",
    @property
    def route_country(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["route_country"]  # type: ignore
            return out
        else:
            return ""

    # "route_city",
    @property
    def route_city(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["route_city"]  # type: ignore
            return out
        else:
            return ""

    # "bc_consumption",
    @property
    def bc_consumption(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["bc_consumption"]  # type: ignore
            return out
        else:
            return ""

    # "bc_avg_speed",
    @property
    def bc_avg_speed(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["bc_avg_speed"]  # type: ignore
            return out
        else:
            return ""

    # "ac",
    @property
    def ac(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["ac"]  # type: ignore
            return out
        else:
            return ""

    # "currency",
    @property
    def currency(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["currency"]  # type: ignore
            return out
        else:
            return ""

    # "fuel_name",
    @property
    def fuel_name(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["fuel_name"]  # type: ignore
            return out
        else:
            return ""

    # "gas_station_name",
    @property
    def gas_station_name(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["gas_station_name"]  # type: ignore
            return out
        else:
            return ""

    def __eq__(self, arg: TMotoStat) -> bool:
        """Equal."""
        return self.date == arg.date

    def __ge__(self, arg: TMotoStat) -> bool:
        """Greater or equal."""
        return self.date >= arg.date

    def __gt__(self, arg: TMotoStat) -> bool:
        """Greater."""
        return self.date > arg.date

    def __le__(self, arg: TMotoStat) -> bool:
        """Less or equal."""
        return self.date <= arg.date

    def __lt__(self, arg: TMotoStat) -> bool:
        """Less."""
        return self.date < arg.date

    def __ne__(self, arg: TMotoStat) -> bool:
        """Negative."""
        return self.date != arg.date


class SpritMonitor(BDebug, BVerbose):
    """SpritMonitor converter class."""

    def __init__(self, item: MotoStat) -> None:
        """Constructor."""


# #[EOF]#######################################################################
