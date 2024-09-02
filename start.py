#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  start.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 2.09.2024, 15:47:48
  
  Purpose: Converter from motostat to spritmonitor.
"""

import sys

from libs.main import Converter


if __name__ == "__main__":
    app = Converter()
    app.run()
    sys.exit(0)

# #[EOF]#######################################################################
