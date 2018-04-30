#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Reading single character by forcing stdin to raw mode
"""

import sys
import tty
import termios


def readchar():
    """
    Read a single character from stdin
    """
    filedes = sys.stdin.fileno()
    old_settings = termios.tcgetattr(filedes)
    try:
        tty.setraw(sys.stdin.fileno())
        character = sys.stdin.read(1)
    finally:
        termios.tcsetattr(filedes, termios.TCSADRAIN, old_settings)
    if ord(character) == 3:
        raise KeyboardInterrupt
    return character


def readkey(getchar_fn=None):
    """
    Reads from stdin but removes escaped characters if they exist
    """
    getchar = getchar_fn or readchar
    char1 = getchar()
    if ord(char1) != 0x1b:  # 27 - Escape
        return char1
    char2 = getchar()
    if ord(char2) != 0x5b:  # 91 - [
        return char1
    char3 = getchar()
    # 16=Up, 17=Down, 18=Right, 19=Left arrows
    return chr(0x10 + ord(char3) - 65)
