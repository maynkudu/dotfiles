#!/usr/bin/env python3
"""Disposable Portless stand-in. Ports are supplied by the fixture, never chosen by production."""

import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import threading


def main():
    directory = Path(os.environ['PORTLESS_STATE_DIR'])
    arguments = sys.argv[1:]
    if len(arguments) < 5 or arguments[:2] != ['run', '--name'] or '--' not in arguments:
        return 3
    name = arguments[2]
    command = arguments[arguments.index('--') + 1:]
    with (directory / 'starts.txt').open('a') as stream:
        stream.write(str(os.getpid()) + '\n')
    behavior = os.environ.get('FIXTURE_PORTLESS_BEHAVIOR', 'normal')
    if behavior == 'fail':
        return 4
    child = subprocess.Popen(command, cwd=Path.cwd(), start_new_session=True)
    stop = threading.Event()
    for signum in (signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, lambda _signal, _frame: stop.set())
    listener = None
    try:
        if behavior != 'slow':
            listener = socket.socket()
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(('127.0.0.1', int(os.environ['FIXTURE_APP_PORT'])))
            listener.listen()
            (directory / 'routes.json').write_text(json.dumps([{'hostname': name + '.localhost',
                'port': int(os.environ['FIXTURE_APP_PORT']), 'pid': os.getpid()}]))
        while not stop.wait(0.05):
            if child.poll() is not None:
                return child.returncode
        return 0
    finally:
        if listener:
            listener.close()
        routes = directory / 'routes.json'
        if routes.exists():
            routes.write_text('[]')
        if child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=1)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=1)


if __name__ == '__main__':
    raise SystemExit(main())
