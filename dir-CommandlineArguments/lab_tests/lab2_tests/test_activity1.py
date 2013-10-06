from __future__ import print_function
import unittest
import os
import subprocess
import glob
import env_settings
from lab_tests.utils_for_testing.autotesting import *
from utils.color import cprint


NOT_TESTABLE = ('Cannot run test. Make sure ShowArgs exists (have you run '
                '"make activity1"?)')

def is_testable(executables=["ShowArgs"]):
    for executable in executables:
        if not os.path.exists(executable):
            return False
    return True


class TestActivity1(unittest.TestCase):
    def test_arg0(self):
        """ShowArgs should print the program name as argument 0."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        self.assertEqual("./ShowArgs\n",
                         subprocess.check_output(['./ShowArgs']))

    def test_print_all_args(self):
        """The program should print all commandline arguments."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        cprint("\nChecking the results from the following command:")
        cprint(color="red",
               msg="  $ ./ShowArgs foo bar baz qux corge grault garply waldo "
                   "fred plugh xyzzy thud ")
        self.assertEqual(subprocess.check_output(
                ['./ShowArgs', 'foo', 'bar', 'baz', 'qux', 'corge', 'grault',
                'garply', 'waldo', 'fred', 'plugh', 'xyzzy', 'thud']),
                "./ShowArgs\nfoo\nbar\nbaz\nqux\ncorge\ngrault\n"
                "garply\nwaldo\nfred\nplugh\nxyzzy\nthud\n")

    def test_memleak(self):
        """It shouldn't have a memory leak."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        if is_memleak('./ShowArgs') or is_memleak('./ShowArgs foo bar'):
            self.fail()

    def test_for_style(self):
        """The code should conform to Google code standards."""
        files = ['main_lab2.cc', 'utilities_lab2.cc', 'definitions_lab2.h']
        self.assertTrue(is_testable(files),
                        "Cannot run test. Make sure {0} exist.".format(files))
        for source in files:
            if is_poor_style('./{0}'.format(source)):
                msg = (
"{0} has style issues. Run the following command to see them:\n"
"  $ python data/cpplint.py {0}".format(source) +
"\nNote: The [legal/copyright] error is ignored.")
                self.fail(msg=msg)

    def test_freshness(self):
        """The executable should be more fresh than all source files."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        path = os.path.realpath(__file__)
        for _ in range(2):  # Split off .../test/test_problem1.py
            path = os.path.split(path)[0]

        last_compile_time = 1
        freshness = 0
        for f in glob.glob(os.path.join(path, "*")):
            if os.path.split(f)[1] == "ShowArgs":
                last_compile_time = os.path.getmtime(f)
            if os.path.split(f)[1].split(".")[0] in ["definitions_lab2",
                                                     "main_lab2",
                                                     "utilities_lab2"]:
                t = os.path.getmtime(f)
                if t > freshness:
                    freshness = t
        if last_compile_time < freshness:
            self.fail("The source files have changed since the last compile."
                      "To fix this, run:\n"
                      "  $ make activity1")

    def test_repository(self):
        """All work should be backed up."""
        if subprocess.check_output(['hg', 'status']):
            cprint("\nFrom the commandline, use the following commands to "
                   "backup your work:")
            cprint(color="red", msg="  $ hg addremove")
            cprint(color="red", msg='  $ hg com -m "This commit message '
                                    'describes what the changeset does using '
                                    'present tense."')

            self.fail("There are uncommitted changes.")

