# -*- coding: utf-8 -*-
"""
  main.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 2.09.2024, 15:49:50
  
  Purpose: The main project class.
"""

from queue import Queue
import os, sys, time, signal

from inspect import currentframe
from typing import Optional, List


from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import CommandLineParser, PathChecker
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.datetool import Timestamp, DateTime
from jsktoolbox.raisetool import Raise
from jsktoolbox.logstool.logs import (
    LoggerEngine,
    LoggerClient,
    LoggerEngineStdout,
    LoggerEngineFile,
    LoggerQueue,
    LogsLevelKeys,
    ThLoggerProcessor,
)
from jsktoolbox.logstool.formatters import LogFormatterNull, LogFormatterDateTime
from jsktoolbox.libs.system import Env

from libs.base import BMiles, BaseApp, BDebug, BVerbose
from libs.processor import CsvProcessor


class Converter(BaseApp, BMiles, BDebug, BVerbose):
    """Main class."""

    def __init__(self) -> None:
        """Constructor."""

        # logging subsystem
        log_engine = LoggerEngine()
        log_queue: Optional[LoggerQueue] = log_engine.logs_queue

        # logger levels
        self.__init_log_levels(log_engine)

        # logger client
        self.logs = LoggerClient()

        # logger processor
        thl = ThLoggerProcessor()
        thl.sleep_period = 0.2
        thl.logger_engine = log_engine
        thl.logger_client = self.logs
        self.logs_processor = thl

        # check command line
        self.__init_command_line()

        # update debug
        self.logs_processor._debug = self.debug

        # signal handling
        signal.signal(signal.SIGTERM, self.__sig_exit)
        signal.signal(signal.SIGINT, self.__sig_exit)

    def run(self) -> None:
        """Run procedure."""

        if self.debug:
            self.logs.message_debug = "test"

        # logger processor
        self.logs_processor.start()

        # init variables
        comms_queue: Queue = Queue()

        # CsvProcessor
        csv_proc = CsvProcessor(
            logger_queue=(
                self.logs.logs_queue
                if self.logs and self.logs.logs_queue
                else LoggerQueue()
            ),
            comms_queue=comms_queue,
            debug=self.debug,
            verbose=self.verbose,
            miles=self.miles,
        )
        # starting CsvProcessor
        csv_proc.start()

        # main procedure
        if not os.isatty(sys.stdin.fileno()):
            line: str = ""
            while not self.stop:
                line += sys.stdin.readline()
                if line == "":
                    break
                # print(line)
                if not line.endswith("\r\n"):
                    comms_queue.put(line)
                    line = ""
        else:
            self.logs.message_info = "Application can read only from STDIN pipe"
            self.logs.message_info = "Example of usage:"
            self.logs.message_info = f"$ cat file.csv|{sys.argv[0]}"

        # exit
        time.sleep(1)

        # stop CsvProcessor
        csv_proc.stop()
        while csv_proc.is_alive():
            time.sleep(0.1)
        csv_proc.join()

        # logger processor
        self.logs_processor.stop()
        while not self.logs_processor.is_stopped:
            self.logs_processor.join()
            time.sleep(0.1)

        sys.exit(0)

    def __sig_exit(self, signum: int, frame) -> None:
        """Received TERM|INT signal."""
        if self.debug:
            self.logs.message_debug = "TERM or INT signal received."
        self.stop = True

    def __init_command_line(self) -> None:
        """Initialize command line."""
        parser = CommandLineParser()

        # configuration for arguments
        parser.configure_argument("h", "help", "this information.")
        parser.configure_argument("d", "debug", "debug flag for debugging.")
        parser.configure_argument("v", "verbose", "verbose flag.")
        parser.configure_argument("m", "miles", "mileage in miles.")

        # command line parsing
        parser.parse_arguments()

        # check
        if parser.get_option("help") is not None:
            self._help(parser.dump())
        if parser.get_option("debug") is not None:
            # set debug flag
            self.debug = True
        if parser.get_option("verbose") is not None:
            # set verbose flag
            self.verbose = True
        if parser.get_option("miles") is not None:
            self.miles = True

    def __init_log_levels(self, engine: LoggerEngine) -> None:
        """Set logging levels configuration for LoggerEngine."""
        # ALERT
        engine.add_engine(
            LogsLevelKeys.ALERT,
            LoggerEngineStdout(
                name=f"{self._c_name}->ALERT",
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )
        # DEBUG
        engine.add_engine(
            LogsLevelKeys.DEBUG,
            LoggerEngineStdout(
                name=f"{self._c_name}->DEBUG",
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )
        # ERROR
        engine.add_engine(
            LogsLevelKeys.ERROR,
            LoggerEngineStdout(
                name=f"{self._c_name}->ERROR",
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )
        # NOTICE
        engine.add_engine(
            LogsLevelKeys.NOTICE,
            LoggerEngineStdout(
                name=f"{self._c_name}->NOTICE",
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )
        lff_notice = LoggerEngineFile(
            name=f"{self._c_name}", formatter=LogFormatterDateTime()
        )
        lff_notice.logdir = "/tmp"
        lff_notice.logfile = "uke-pit-spider.NOTICE.log"
        engine.add_engine(
            LogsLevelKeys.NOTICE,
            lff_notice,
        )

        # CRITICAL
        engine.add_engine(
            LogsLevelKeys.CRITICAL,
            LoggerEngineStdout(
                name=f"{self._c_name}->CRITICAL",
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )
        lff_critical = LoggerEngineFile(
            name=f"{self._c_name}", formatter=LogFormatterDateTime()
        )
        lff_critical.logdir = "/tmp"
        lff_critical.logfile = "uke-pit-spider.CRITICAL.log"
        engine.add_engine(
            LogsLevelKeys.CRITICAL,
            lff_critical,
        )
        # EMERGENCY
        engine.add_engine(
            LogsLevelKeys.EMERGENCY,
            LoggerEngineStdout(
                name=f"{self._c_name}->EMERGENCY",
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )
        # INFO
        engine.add_engine(
            LogsLevelKeys.INFO,
            LoggerEngineStdout(
                name=self._c_name,
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )
        # WARNING
        engine.add_engine(
            LogsLevelKeys.WARNING,
            LoggerEngineStdout(
                name=f"{self._c_name}->WARNING",
                # formatter=LogFormatterDateTime(),
                formatter=LogFormatterNull(),
            ),
        )


# #[EOF]#######################################################################
