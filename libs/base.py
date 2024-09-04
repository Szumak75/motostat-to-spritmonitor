# -*- coding: utf-8 -*-
"""
  base.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 2.09.2024, 15:57:58
  
  Purpose: Base class for project.
"""

import sys

from typing import List, Dict

from jsktoolbox.libs.base_data import BData
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.logstool.logs import LoggerClient, ThLoggerProcessor


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal _Keys container class."""

    COMMAND_LINE_OPTS: str = "__clo__"
    DEBUG: str = "__debug__"
    DIR: str = "__dir__"
    LOGGER_CLIENT: str = "__logger_client__"
    MILES: str = "__miles__"
    PROC_LOGS: str = "__logger_processor__"
    SET_STOP: str = "__set_stop__"
    VERBOSE: str = "__verbose__"


class BDebug(BData):
    """Base class for debugging property."""

    @property
    def debug(self) -> bool:
        """Returns debug flag."""
        return self._get_data(
            key=_Keys.DEBUG, set_default_type=bool, default_value=False
        )  # type: ignore

    @debug.setter
    def debug(self, flag: bool) -> None:
        """Sets debug flag."""
        self._set_data(key=_Keys.DEBUG, value=flag)


class BVerbose(BData):
    """Base class for verbose debugging property."""

    @property
    def verbose(self) -> bool:
        """Returns debug flag."""
        return self._get_data(
            key=_Keys.VERBOSE, set_default_type=bool, default_value=False
        )  # type: ignore

    @verbose.setter
    def verbose(self, flag: bool) -> None:
        """Sets debug flag."""
        self._set_data(key=_Keys.VERBOSE, set_default_type=bool, value=flag)


class BLogs(BData):
    """Base class for LoggerClient property."""

    @property
    def logs(self) -> LoggerClient:
        """Returns LoggerClient object."""
        return self._get_data(
            key=_Keys.LOGGER_CLIENT,
            set_default_type=LoggerClient,
            default_value=LoggerClient(),
        )  # type: ignore

    @logs.setter
    def logs(self, logger_client: LoggerClient) -> None:
        """Sets LoggerClient."""
        self._set_data(key=_Keys.LOGGER_CLIENT, value=logger_client)


class BStop(BData):
    """Base class for stop method."""

    @property
    def stop(self) -> bool:
        """Returns STOP flag."""
        return self._get_data(
            key=_Keys.SET_STOP, set_default_type=bool, default_value=False
        )  # type: ignore

    @stop.setter
    def stop(self, flag: bool) -> None:
        """Sets STOP flag."""
        self._set_data(key=_Keys.SET_STOP, value=flag)


class BMiles(BData):
    """Base class for MILES flag."""

    @property
    def miles(self) -> bool:
        """Returns miles flag."""
        return self._get_data(
            key=_Keys.MILES, set_default_type=bool, default_value=False
        )  # type: ignore

    @miles.setter
    def miles(self, value: bool) -> None:
        """Sets miles flag."""
        self._set_data(key=_Keys.MILES, set_default_type=bool, value=value)


class BDir(BData):
    """Base class for output dir."""

    @property
    def output_dir(self) -> str:
        """Returns output_dir str."""
        return self._get_data(
            key=_Keys.DIR, set_default_type=str, default_value="/tmp"
        )  # type: ignore

    @output_dir.setter
    def output_dir(self, value: str) -> None:
        """Sets output_dir str."""
        self._set_data(key=_Keys.DIR, set_default_type=str, value=value)


class BaseApp(BLogs, BStop):
    """Main app base class."""

    @property
    def command_opts(self) -> bool:
        """Returns commands line flag"""
        return self._get_data(
            key=_Keys.COMMAND_LINE_OPTS, set_default_type=bool, default_value=False
        )  # type: ignore

    @command_opts.setter
    def command_opts(self, flag: bool) -> None:
        """Sets commands line flag."""
        self._set_data(key=_Keys.COMMAND_LINE_OPTS, value=flag)

    @property
    def logs_processor(self) -> ThLoggerProcessor:
        """Return logs_processor."""
        return self._get_data(
            key=_Keys.PROC_LOGS, set_default_type=ThLoggerProcessor
        )  # type: ignore

    @logs_processor.setter
    def logs_processor(self, value: ThLoggerProcessor) -> None:
        """Set logs_processor."""
        self._set_data(key=_Keys.PROC_LOGS, value=value)

    def _help(self, command_conf: Dict) -> None:
        """Show help information and shutdown."""
        command_opts: str = ""
        desc_opts: List = []
        max_len: int = 0
        opt_value: List = []
        opt_no_value: List = []
        # stage 1
        for item in command_conf.keys():
            if max_len < len(item):
                max_len = len(item)
            if command_conf[item]["has_value"]:
                opt_value.append(item)
            else:
                opt_no_value.append(item)
        max_len += 7
        # stage 2
        for item in sorted(opt_no_value):
            tmp: str = ""
            if command_conf[item]["short"]:
                tmp = f"-{command_conf[item]['short']}|--{item} "
            else:
                tmp = f"--{item}    "
            desc_opts.append(f" {tmp:<{max_len}}- {command_conf[item]['description']}")
            command_opts += tmp
        # stage 3
        for item in sorted(opt_value):
            tmp: str = ""
            if command_conf[item]["short"]:
                tmp = f"-{command_conf[item]['short']}|--{item}"
            else:
                tmp = f"--{item}   "
            desc_opts.append(f" {tmp:<{max_len}}- {command_conf[item]['description']}")
            command_opts += tmp
            if command_conf[item]["example"]:
                command_opts += f"{command_conf[item]['example']}"
            command_opts += " "
        print("###[HELP]###")
        print(f"{sys.argv[0]} {command_opts}")
        print(f"")
        print("# Arguments:")
        for item in desc_opts:
            print(item)
        sys.exit(2)


# #[EOF]#######################################################################
