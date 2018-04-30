#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Sets the logger to use a console with a default minimum level of INFO
using the following format:
[2018-04-08 20:52:14.755] [INFO    ]        ServoController.py:38:<MainThread>
   Setting up ServoController Module
"""

import logging
import colorlog


def setup_console_logger(logger_name, level=logging.INFO):
    """
    Setup a console based logger
    :param logger_name: The logger to attach to
    :param level: The minimum level to show. This defaults to ignore DEBUG
    :return: N/A
    """
    logger_name.setLevel(logging.DEBUG)
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(level)
    formatter = colorlog.ColoredFormatter(
        "[%(asctime)s.%(msecs)03d] %(log_color)s[%(levelname)-8s]%(reset)s "
        "%(filename)25s:%(lineno)d:<%(threadName)s>\t "
        "%(log_color)s%(message)s", "%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    logger_name.addHandler(console_handler)
