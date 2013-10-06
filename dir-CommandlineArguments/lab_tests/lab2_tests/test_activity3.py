from __future__ import print_function
import unittest
import os
import subprocess
import glob
import env_settings
from lab_tests.utils_for_testing.autotesting import *
from utils.color import cprint

NOT_TESTABLE = ('Cannot run test. Make sure \'calc\' exists (have you run '
                '"make activity3"?)')

def is_testable(executables=["calc"]):
    for executable in executables:
        if not os.path.exists(executable):
            return False
    return True


def evaluate_op(trials):
    """This evaluates calc using the list of parameters."""
    for trial in trials:
        try:
            res = subprocess.check_output(['./calc'] + list(trial[1]))
        except subprocess.CalledProcessError as e:
            return ("calc was unable to handle the following "
                    "arguments: {0}".format(' '.join(trial[1])))
        try:
            if ((float(res) + 0.05 <= float(res)) or
                (float(res) - 0.05 >= float(res))):
                return ("Unexpected result. Input: {0} Output: {1}"
                        "Expected: {2}".format(' '.join(trial[1]),
                                               res, trial[0]))
        except AttributeError:
            return ("calc did not return a number when given the following "
                    "arguments: {0}".format(' '.join(trial[1])))


class TestActivity3(unittest.TestCase):
    """This tests the functionality of a basic calculator."""
    def test_too_few_args(self):
        """It should exit with the value '17' when given too few args."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        args = ["spam", "eggs"]
        for i in range(len(args)):
            try:
                subprocess.check_call(['./calc'] + args[:i])
                self.fail("The calc program did not return an error code when "
                          "too few arguments were supplied.")
            except subprocess.CalledProcessError as e:
                if e.returncode == 17:
                    continue
                else:
                    self.fail("Unexpected error code was returned.")

    def test_three_plus_args(self):
        """It should exit with the value '17' when given more than 3 args."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        args = ['6', '+', '6', '-', '1', 'foo', 'bar', 'baz', 'qux', 'corge',
                'grault', 'garply', 'waldo', 'fred', 'plugh', 'xyzzy', 'thud']
        for i in range(4, len(args)):
            try:
                subprocess.check_call(['./calc'] + args[:i])
                self.fail("calc didn't exit with code 17 upon "
                          "{0} arguments.".format(i))
            except:
                continue

    # Requiring the testing of bad args requires strtod, which requires
    # pointers. This is beyond the scope of the lab.
    '''
    def test_bad_args(self):
        """It should exit with the value '17' when given unhandleable args."""
        trials = [['./calc', 'two', 'times', 'three'],
                  ['./calc', '2', '**', '3'],
                  ['./calc', '*', '*', '?'],
                  ['./calc', '43.32', '?', '-25']]
        for trial in trials:
            try:
                subprocess.check_call(trial)
                self.fail("calc did not return '17' when given these bad"
                          " arguments: {0}".format(' '.join(trial)))
            except subprocess.CalledProcessError as e:
                if e.returncode != 17:
                    self.fail("An unexpected error code was returned.")
    '''

    def test_add(self):
        """It should correctly add values."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        trials = [('0', ['-4', '+', '4']),
                  ('3', ['0', '+', '3']),
                  ('4.5', ['4', '+', '0.5']),
                  ('4.5', ['4', '+', '.5']),
                  ('-13.2', ['-15', '+', '1.8'])]
        res = evaluate_op(trials)
        if res:
            self.fail(res)

    def test_subtract(self):
        """It should correctly subtract values."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        trials = [('0', ['4', '-', '4']),
                  ('-3', ['0', '-', '3']),
                  ('-42', ['43', '-', '85']),
                  ('13.38', ['15', '-', '1.62']),
                  ('-1024', ['-512', '-', '512']),
                  ('0', ['-512', '-', '-512'])]
        res = evaluate_op(trials)
        if res:
            self.fail(res)

    def test_multiply(self):
        """It should correctly multiply values."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        trials = [('0', ['9', '*', '0']),
                  ('8', ['2', '*', '4']),
                  ('6', ['3', '*', '2']),
                  ('-52', ['-1', '*', '52']),
                  ('1344', ['42.00', '*', '32']),
                  ('1.32', ['1.1', '*', '1.2']),
                  ('21.025', ['-1.45', '*', '-14.5'])]
        res = evaluate_op(trials)
        if res:
            self.fail(res)

    def test_divide(self):
        """It should correctly divide values."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        trials = [('0', ['0', '/', '8']),
                  ('1', ['9.9', '/', '9.9']),
                  ('-4', ['-16', '/', '4']),
                  ('-4', ['16', '/', '-4']),
                  ('0.25', ['-1', '/', '-4'])]
        res = evaluate_op(trials)
        if res:
            self.fail(res)

    def test_modulo(self):
        """It should correctly take the modulo of values."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        trials = [('0', ['0', '%', '8']),
                  ('1', ['3', '%', '2']),
                  ('2', ['2', '%', '3']),
                  ('2', ['5', '%', '3']),
                  ('2', ['-1', '%', '3']),
                  ('0', ['1337', '%', '1337']),
                  ('9001', ['19000', '%', '9999']),
                  ('99', ['10000099', '%', '100'])]
        res = evaluate_op(trials)
        if res:
            self.fail(res)

    def test_illegal_opperations(self):
        """It should return '17' when requested to perform an illegal op."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        trials = [['7', '%', '0'],
                  ['8', '/', '0']]
        for trial in trials:
            try:
                subprocess.check_call(['./calc'] + trial)
            except subprocess.CalledProcessError as e:
                if e.returncode == 17:
                    continue
            self.fail("calc did not exit with the code '17' on this illegal "
                      "op: {0}".format(" ".join(trial)))

    def test_memleak(self):
        """It shouldn't have a memory leak."""
        self.assertTrue(is_testable(), NOT_TESTABLE)
        if is_memleak('./calc 2 * 3'):
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
        path = os.path.realpath(__file__)
        for _ in range(2):  # Split off .../test/test_problem1.py
            path = os.path.split(path)[0]

        last_compile_time = 1
        freshness = 0
        for f in glob.glob(os.path.join(path, "*")):
            if os.path.split(f)[1] == "calc":
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
