#!/usr/bin/env python
from flow.command import CommandHandler

try:
    import settings # assuming it's in the same directory
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r.\nIf the file settings.py does indeed exist, it's causing an ImportError somehow.\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    c = CommandHandler()
    c.run_command()
