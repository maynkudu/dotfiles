#!/usr/bin/env python3
"""Disposable command tree with an independently grouped child for shutdown tests."""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading


def main():
    child = subprocess.Popen([sys.executable, '-c', 'import signal; signal.pause()'], start_new_session=True)
    Path(os.environ['FIXTURE_TREE_FILE']).write_text(json.dumps({'parent': os.getpid(), 'child': child.pid}))
    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda _signal, _frame: stop.set())
    signal.signal(signal.SIGINT, lambda _signal, _frame: stop.set())
    try:
        stop.wait()
    finally:
        # Leave the independently grouped child to the owned supervisor, which is the behavior under test.
        pass


if __name__ == '__main__':
    main()
