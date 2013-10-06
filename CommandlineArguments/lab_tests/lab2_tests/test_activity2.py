from __future__ import print_function
import unittest
import os
import subprocess
import glob
import env_settings
from lab_tests.utils_for_testing.autotesting import *
from utils.color import cprint

NOT_TESTABLE = ('Cannot run test. Make sure \'Act2\' exists (have you run '
                '"make activity2"?)')

def is_testable(executables=["Act2"]):
    for executable in executables:
        if not os.path.exists(executable):
            return False
    return True

class TestActivity2(unittest.TestCase):
    """This tests that Act2 checks the number of commandline args."""
    def test_two_args(self):
        """It should exit with the value '17' when given 2 args."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        try:
            subprocess.check_call(['./Act2', 'spam', 'eggs'])
        except subprocess.CalledProcessError as e:
            if e.returncode == 17:
                return
        self.fail('"./Act2 spam eggs" did not return the expected error code.')

    def test_three_plus_args(self):
        """It should exit with the value '0' when given more than 2 args."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        args = ['foo', 'bar', 'baz', 'qux', 'corge', 'grault', 'garply',
                'waldo', 'fred', 'plugh', 'xyzzy', 'thud']
        for i in range(3, len(args)):
            try:
                self.assertEqual(0,
                                 subprocess.check_call(['./Act2'] + args[:i]))
            except:
                self.fail("Act2 was displeased with {0} arguments.".format(i))

    def test_memleak(self):
        """It shouldn't have a memory leak."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        if (is_memleak('./Act2') or is_memleak('./Act2 foo bar') or
            is_memleak('./Act2 foo bar baz thud')):
            self.fail()

    def test_for_style(self):
        """The code should conform to Google code standards."""
        files = ['main_lab2.cc', 'utilities_lab2.cc', 'definitions_lab2.h']
        self.assertTrue(is_testable(files),
                        "One of the following is missing: {0}".format(files))
        for source in files:
            if is_poor_style('./{0}'.format(source)):
                msg = (
"{0} has style issues. Run the following command to see them:\n"
"  $ python data/cpplint.py {0}".format(source) +
"\nNote: The [legal/copyright] error is ignored.")
                self.fail(msg=msg)

    def test_freshness(self):
        """The executable should be more fresh than all source files."""
        files = ['main_lab2.cc', 'utilities_lab2.cc', 'definitions_lab2.h']
        self.assertTrue(is_testable(files),
                        "One of the following is missing: {0}".format(files))
        path = os.path.realpath(__file__)
        for _ in range(2):  # Split off .../test/test_problem1.py
            path = os.path.split(path)[0]

        last_compile_time = 1
        freshness = 0
        for f in glob.glob(os.path.join(path, "*")):
            if os.path.split(f)[1] == "Act2":
                last_compile_time = os.path.getmtime(f)
            if os.path.split(f)[1].split(".")[0] in files:
                t = os.path.getmtime(f)
                if t > freshness:
                    freshness = t
        if last_compile_time < freshness:
            self.fail("The source files have changed since the last compile."
                      "To fix this, run:\n"
                      "  $ make activity2")

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
