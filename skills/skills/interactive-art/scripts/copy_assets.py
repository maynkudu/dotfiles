#!/usr/bin/env python3
"""Copy editable scene modules into a new directory in the host project."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--react', action='store_true', help='Include the React component example.')
    args = parser.parse_args()
    destination = args.destination.expanduser().resolve()
    assets = Path(__file__).resolve().parents[1] / 'assets'
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        parser.error(f'Destination must be an empty directory: {destination}')
    destination.mkdir(parents=True, exist_ok=True)
    for name in ('engine', 'scenes') + (('examples',) if args.react else ()):
        shutil.copytree(assets / name, destination / name)
    print(f'Copied scene modules to {destination}')


if __name__ == '__main__':
    main()
