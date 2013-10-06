import inspect
import os
import sys

if not sys.version.startswith("2.7"):
    assert False, "No suitable Python installation was found."

try:
    import nose
except ImportError:
    print "No suitable installation of the module 'nose' was found."
    print
    raise

try:
    import rednose
except ImportError:
    print "No suitable installation of the module 'rednose' was found."
    print
    raise

CUR_FILE = os.path.abspath(inspect.getfile(inspect.currentframe()))
CUR_DIR = os.path.split(CUR_FILE)[0]
TESTING_DIR = os.path.split(CUR_DIR)[0]
SOURCE_DIR = os.path.split(TESTING_DIR)[0]
sys.path.append(SOURCE_DIR)

