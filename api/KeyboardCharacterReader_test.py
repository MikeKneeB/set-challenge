#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Provides the test functionality for the keyboard reader
"""

import logging
import SetupConsoleLogger
import KeyboardCharacterReader

MODULE_LOGGER = logging.getLogger("__main__")
SetupConsoleLogger.setup_console_logger(MODULE_LOGGER)


def test_keyboard_character_reader():
    """
    keyboard reader test
    """

    try:
        while True:
            keyp = KeyboardCharacterReader.readkey()
            if ord(keyp) == 16:
                MODULE_LOGGER.info("up")
            elif ord(keyp) == 17:
                MODULE_LOGGER.info("down")
            elif ord(keyp) == 19:
                MODULE_LOGGER.info("left")
            elif ord(keyp) == 18:
                MODULE_LOGGER.info("right")
            elif keyp == ' ':
                MODULE_LOGGER.info("space")
            else:
                MODULE_LOGGER.info(
                    "key: " + str(keyp) + " (" + str(ord(keyp)) + ")")

    except KeyboardInterrupt:
        pass
    finally:
        pass


if __name__ == "__main__":
    test_keyboard_character_reader()
