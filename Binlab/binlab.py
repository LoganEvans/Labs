#!/usr/bin/env python
"""
This is the indended entry point to binlab. Start the program from the
commandline with

 $ python -i binlab.py

"""

from binary import ComplimentBinary, SignedMagnitude
from binary import UnsignedBinary, GrayCode


if __name__ == '__main__':
    import code
    code.interact(local=locals())

