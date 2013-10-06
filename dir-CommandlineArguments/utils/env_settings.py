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

cur_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
UTILS_DIR = os.path.split(cur_file)[0]
SOURCE_DIR = os.path.split(UTILS_DIR)[0]
TESTS_DIR = os.path.join(SOURCE_DIR, "lab_tests")
BOILERPLATES_DIR = os.path.join(SOURCE_DIR, "lab_boilerplates")
UTILS_DIR = os.path.join(SOURCE_DIR, "utils")

print 'appending...', SOURCE_DIR
sys.path.append(SOURCE_DIR)

