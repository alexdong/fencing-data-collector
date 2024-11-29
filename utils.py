#!/usr/bin/env python3
import sys
import termios
import tty
import select
from typing import Optional


def get_char_timeout(timeout: float) -> Optional[str]:
    """Get a single character input with timeout.

    Args:
        timeout: Number of seconds to wait for input

    Returns:
        The character read or None if timeout occurs
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        return sys.stdin.read(1) if rlist else None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
