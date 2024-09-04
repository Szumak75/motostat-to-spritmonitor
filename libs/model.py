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
from datetime import datetime


from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue
from jsktoolbox.libs.base_th import ThBaseObject
from jsktoolbox.netaddresstool.ipv4 import Address, Network
from jsktoolbox.raisetool import Raise
from jsktoolbox.devices.network.connectors import API
from jsktoolbox.devices.mikrotik.routerboard import RouterBoard
from jsktoolbox.datetool import Timestamp

from libs.base import BDebug, BMiles, BVerbose, BLogs, BStop

TMotoStat = TypeVar("TMotoStat", bound="MotoStat")


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal keys class."""

    CSV_COST: str = "__cost__"
    CSV_FUEL: str = "__fuel__"
    DATA: str = "__data__"
    FUELING: str = "__fueling__"


class MotoStat(BDebug, BVerbose, BMiles):
    """MotoStat data class."""

    def __init__(self, csv_line: str, miles: bool = False) -> None:
        """Constructor."""
        self.miles = miles
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
            if out:
                if self.miles:
                    x: float = float(out) * 0.621371192
                    return f"{x:.0f}"
                else:
                    return out
            return out
        else:
            return ""

    # "trip_odometer",
    @property
    def trip_odometer(self) -> str:
        if self._get_data(key=_Keys.DATA, default_value={}):
            out: str = self._get_data(key=_Keys.DATA)["trip_odometer"]  # type: ignore
            if out:
                if self.miles:
                    x: float = float(out) * 0.621371192
                    return f"{round(x,0):.2f}"
                else:
                    return f"{float(out):.2f}"
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
            return out.strip('"')
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

    @property
    def gas(self) -> bool:
        """Returns True if fuel is LPG/CNG."""
        if self.fuel_name:
            if "LPG" in self.fuel_name or "CNG" in self.fuel_name:
                return True
        return False

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
    """SpritMonitor converter class.

    ### Fuelings CSV
        Date: Format DD.MM.YYYY (e.g., 23.02.2010)
        Odometer, distance, quantity, total price: Numeric without thousands separator
        Currency: Standard abbreviation (e.g., EUR, USD)
        Fueling type: 0=invalid fueling, 1=full fueling, 2=partial fueling, 3=first fueling
        Tires: 1=summer tires, 2=winter tires, 3=all-year tires
        Roads: Sum of 2=motor-way, 4=city, 8=country roads (e.g., motor-way and country roads: 10)
        Driving style: 1=moderate, 2=normal, 3=fast
        Fuel sort: 1=Diesel, 2=Biodiesel, 3=Vegetable oil, 4=Premium Diesel, 6=Normal gasoline, 7=Super gasoline, 8=SuperPlus gasoline, 9=Premium Gasoline 100, 12=LPG, 13=CNG H, 14=CNG L, 15=Bio-alcohol, 16=Two-stroke, 18=Premium Gasoline 95, 19=Electricity, 20=E10, 21=AdBlue, 22=Premium Gasoline 100+, 23=Hydrogen, 24=Green electricity, 25=GTL Diesel, 26=HVO100
        Note: Text
        Consumption, BC-consumption, BC-quantity, BC-speed: Numeric without thousands separator
        Company, Country, Area, Location: Text

    ### Costs CSV
        Date: Format DD.MM.YYYY (e.g., 23.02.2010)
        Odometer, trip: Numeric without thousands separator
        Type:: 1=Maintenance, 2=Repair, 3=Change tires, 4=Change oil, 5=Insurance, 6=Tax, 7=Supervisory board, 8=Tuning, 9=Accessories, 10=Purchase price, 11=Miscellaneous, 12=Care, 13=Payment, 14=Registration, 15=Financing, 16=Refund, 17=Fine, 18=Parking tax, 19=Toll, 20=Spare parts, 21=Basic charging fee
        Note: Text

    """

    def __init__(self, item: MotoStat) -> None:
        """Constructor."""
        fueling_header: List[str] = [
            "Date",
            "Odometer",
            "Trip",
            "Quantity",
            "Total price",
            "Currency",
            "Type",
            "Tires",
            "Roads",
            "Driving style",
            "Fuel",
            "Note",
            "Consumption",
            "BC-Consumption",
            "BC-Quantity",
            "BC-Speed",
            "Company",
            "Country",
            "Area",
            "Location",
        ]
        self._set_data(key=_Keys.CSV_FUEL, set_default_type=List, value=fueling_header)

        cost_header: List[str] = [
            "Date",
            "Odometer",
            "Cost type",
            "Total price",
            "Currency",
            "Note",
        ]
        self._set_data(key=_Keys.CSV_COST, set_default_type=List, value=cost_header)

        if item.cost_id:
            # new cost
            self.fueling = False
            data: Dict[str, str] = {}
            for key in cost_header:
                data[key] = ""
            self._set_data(key=_Keys.DATA, set_default_type=Dict, value=data)
            self.__add_cost(item)
        if item.fuel_id:
            self.fueling = True
            data: Dict[str, str] = {}
            for key in fueling_header:
                data[key] = ""
            self._set_data(key=_Keys.DATA, set_default_type=Dict, value=data)
            self.__add_fueling(item)

    def __repr__(self) -> str:
        tmp = ""
        for i, v in self._get_data(key=_Keys.DATA).items():  # type: ignore
            tmp += f"'{i}':{v},"
        return f"{self._c_name}({tmp})"

    def __add_fueling(self, item: MotoStat) -> None:
        """Add data to dict."""
        data: Dict[str, str] = self._get_data(
            key=_Keys.DATA,
        )  # type: ignore
        # "Date",
        date_tmp = datetime.fromtimestamp(item.date)
        data["Date"] = f"{date_tmp.day:02d}.{date_tmp.month:02d}.{date_tmp.year}"
        # "Odometer",
        tmp = item.odometer
        if tmp == "0":
            tmp = "0,00"
        else:
            tmp += ",00"
        data["Odometer"] = tmp
        # "Trip",
        data["Trip"] = item.trip_odometer.replace(".", ",")
        # "Quantity",
        data["Quantity"] = item.quantity.replace(".", ",")
        # "Total price",
        data["Total price"] = item.cost.replace(".", ",")
        # "Currency",
        data["Currency"] = item.currency

        # "Type",
        # Fueling type: 0=invalid fueling, 1=full fueling, 2=partial fueling, 3=first fueling
        fueling_dict: Dict[str, str] = {
            "full": "1",
            "partial": "2",
        }
        if float(item.trip_odometer) == 0:
            data["Type"] = "3"
        else:
            data["Type"] = fueling_dict[item.fueling_type]
        # "Tires",
        # Tires: 1=summer tires, 2=winter tires, 3=all-year tires
        tires_dict: Dict[str, str] = {"full_year": "3", "summer": "1", "winter": "2"}
        if item.tires in tires_dict.keys():
            data["Tires"] = tires_dict[item.tires]

        # "Roads",
        # Roads: Sum of 2=motor-way, 4=city, 8=country roads (e.g., motor-way and country roads: 10)
        count = 0
        if float(item.route_city) > 0:
            count += 4
        if float(item.route_motorway) > 0:
            count += 2
        if float(item.route_country) > 0:
            count += 8
        data["Roads"] = f"{count}"

        # "Driving style",
        # Driving style: 1=moderate, 2=normal, 3=fast
        driving_dict: Dict[str, str] = {"normal": "2", "speedy": "3", "economical": "1"}
        data["Driving style"] = driving_dict[item.driving_style]

        # "Fuel",
        # Fuel sort: 1=Diesel, 2=Biodiesel, 3=Vegetable oil, 4=Premium Diesel,
        # 6=Normal gasoline, 7=Super gasoline, 8=SuperPlus gasoline,
        # 9=Premium Gasoline 100, 12=LPG, 13=CNG H, 14=CNG L, 15=Bio-alcohol,
        # 16=Two-stroke, 18=Premium Gasoline 95, 19=Electricity, 20=E10, 21=AdBlue,
        # 22=Premium Gasoline 100+, 23=Hydrogen, 24=Green electricity, 25=GTL Diesel, 26=HVO100
        fuel_dict: Dict[str, str] = {
            "Eurosuper 95": "6",
            "Statoil SupraGaz": "18",
            "LPG": "12",
            "inny gaz LPG": "12",
            "CNG": "14",
            "95 miles": "6",
            "inna benzyna": "6",
            "Super Plus 98": "8",
            "Shell V-Power": "18",
            '"Eurosuper 95"': "6",
            '"Statoil SupraGaz"': "18",
            '"LPG"': "12",
            '"inny gaz LPG"': "12",
            '"CNG"': "14",
            '"95 miles"': "6",
            '"inna benzyna"': "6",
            '"Super Plus 98"': "8",
            '"Shell V-Power"': "18",
        }
        if item.fuel_name in fuel_dict.keys():
            data["Fuel"] = fuel_dict[item.fuel_name]
        # "Note",
        data["Note"] = f'"{item.notes}"'
        # "Consumption",
        if float(item.trip_odometer) > 0:
            tmp = float(item.quantity) * 100 / float(item.trip_odometer)
            data["Consumption"] = f"{tmp:.2f}".replace(".", ",")

        # "BC-Consumption",
        # "BC-Quantity",
        # "BC-Speed",
        # "Company",
        data["Company"] = f'"{item.gas_station_name}"'
        # "Country",
        if item.currency == "PLN":
            data["Country"] = '"PL"'
        # "Area",
        data["Area"] = '""'
        # "Location",
        data["Location"] = '""'
        self._set_data(key=_Keys.DATA, value=data)
        # print(self._get_data(key=_Keys.DATA))

    def __add_cost(self, item: MotoStat) -> None:
        """Add data to dict."""
        cost_type: Dict[str, str] = {
            "maintenance": "1",
            "repair": "2",
            "tires_change": "3",
            "oil_change": "4",
            "insurance": "5",
            "tax": "6",
            "tuning": "8",
            "accessories": "9",
            "purchase_price": "10",
            "miscellaneous": "11",
            "tech_inspection": "11",
            "car_audio": "9",
            "inspection": "11",
            "care": "12",
            "registration": "14",
            "fine": "17",
            "parking_tax": "18",
            "toll": "19",
            "spare_parts": "20",
        }
        data: Dict[str, str] = self._get_data(
            key=_Keys.DATA,
        )  # type: ignore
        # "Date",
        date_tmp: datetime = datetime.fromtimestamp(item.date)
        data["Date"] = f"{date_tmp.day:02d}.{date_tmp.month:02d}.{date_tmp.year}"
        # "Odometer",
        tmp = item.odometer
        if tmp == "0":
            tmp = "0,00"
        else:
            tmp += ",00"
        data["Odometer"] = tmp
        # "Cost type",
        # Type:: 1=Maintenance,
        # 2=Repair,
        # 3=Change tires,
        # 4=Change oil,
        # 5=Insurance,
        # 6=Tax,
        # 7=Supervisory board,
        # 8=Tuning,
        # 9=Accessories,
        # 10=Purchase price,
        # 11=Miscellaneous,
        # 12=Care,
        # 13=Payment,
        # 14=Registration,
        # 15=Financing,
        # 16=Refund,
        # 17=Fine,
        # 18=Parking tax,
        # 19=Toll,
        # 20=Spare parts,
        # 21=Basic charging fee
        if item.cost_type in cost_type.keys():
            data["Cost type"] = cost_type[item.cost_type]
        else:
            data["Cost type"] = "11"
        # "Total price",
        tmp = item.cost
        if tmp == "0":
            tmp = "0,00"
        else:
            tmp = tmp.replace(".", ",")
        data["Total price"] = tmp
        # "Currency",
        data["Currency"] = f'"{item.currency}"'
        # "Note",
        if item.notes:
            data["Note"] = item.notes
        else:
            data["Note"] = '""'
        self._set_data(key=_Keys.DATA, value=data)
        # print(self._get_data(key=_Keys.DATA))

    @property
    def fueling(self) -> bool:
        """Returns FUELING flag."""
        return self._get_data(
            key=_Keys.FUELING, set_default_type=bool, default_value=False
        )  # type: ignore

    @fueling.setter
    def fueling(self, value: bool) -> None:
        """Sets fueling flag."""
        self._set_data(key=_Keys.FUELING, set_default_type=bool, value=value)

    @property
    def header(self) -> List[str]:
        """Returns csv header string."""
        length: int = len(self._get_data(key=_Keys.DATA).keys())  # type: ignore
        if len(self._get_data(key=_Keys.CSV_COST)) == length:  # type: ignore
            return self._get_data(key=_Keys.CSV_COST)  # type: ignore
        else:
            return self._get_data(key=_Keys.CSV_FUEL)  # type: ignore

    @property
    def csv_header(self) -> str:
        """Returns csv header"""
        tmp: str = ""
        for item in self.header:
            if tmp == "":
                tmp += item
            else:
                tmp += f";{item}"
        return tmp

    @property
    def csv_data(self) -> str:
        """Returns csv header"""
        tmp: str = ""
        for item in self.header:
            if tmp == "":
                tmp += self._get_data(key=_Keys.DATA)[item]  # type: ignore
            else:
                tmp += f";{self._get_data(key=_Keys.DATA)[item]}"  # type: ignore
        return tmp


# #[EOF]#######################################################################
