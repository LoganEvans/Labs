Python packages used in development
------------------------------------
 * nose -- A testing package
 * rednose -- Colorizes the nosetests output
 * sphinx -- Documentation tool

Run unittests
------------------
    After the package 'nose' is installed (e.g., with "pip install nose")
    the tests can be run using the following command:

  $ nosetests -v

    Note: Due to the display features of binlab, using the '-s' option will
          drastically increase the amount of time it takes to display all
          tests.

Example
-----------
    From the commandline, execute:

  $ python -i binary.py

>>> dir()
['BaseBinary', 'ComplimentBinary', 'GrayCode', 'SignedMagnitude', 'UnsignedBinary', '__builtins__', '__doc__', '__name__', '__package__']
>>> CB1 = ComplimentBinary(3)
>>> CB2 = ComplimentBinary(-44)
>>> CB3 = CB1 + CB2
----------------------------------------------------------------------------------------------------
| Encoding         |      Binary Value |     Integer Value | Hexadecimal Value |       Octal Value |
|------------------|-------------------|-------------------|-------------------|-------------------|
| ComplimentBinary |          00000011 |                 3 |               0x3 |                03 |
| ComplimentBinary | +        11010100 | +             -44 | +           -0x2c | +            -054 |
|------------------|-------------------|-------------------|-------------------|-------------------|
| ComplimentBinary |          11010111 |               -41 |             -0x29 |              -051 |
----------------------------------------------------------------------------------------------------
>>> print CB3
11010111
>>> for i in range(10):
...     print GrayCode(i)
...
00000000
00000001
00000011
00000010
00000110
00000111
00000101
00000100
00001100
00001101
>>> exit()
