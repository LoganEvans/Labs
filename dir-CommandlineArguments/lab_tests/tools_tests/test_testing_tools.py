import unittest
import autotesting as uut
import subprocess
import glob
import os

class TestCommandline(unittest.TestCase):
    """This confirms that the tools used to test the labs work."""

    def tearDown(self):
        """Removes any side-effect files."""
        testing_dir = os.path.split(os.path.realpath(__file__))[0]
        for f in glob.glob(os.path.join(testing_dir, "*")):
            if f.split(".")[-1] in ["o", "out", "pyc", "log"]:
                subprocess.call(['rm', f])

    def test_testing(self):
        """Testing should work."""

    def test_subprocess_calls(self):
        """The subprocess calls should work."""
        self.assertTrue(uut.get_stdout(['echo', 'this']) == 'this\n')
        self.assertTrue(
                uut.get_outstreams(['python', 'test/str_in_stdout_stderr.py']) ==
                ["In stdout.\n", "In stderr.\n", 17])

    def test_is_memleak(self):
        """The program should print out all args."""
        subprocess.call(
                ["g++", "-g", "test/with_leak.cc", "-o", "test/leaky.out"])
        self.assertTrue(uut.is_memleak("test/leaky.out"))
        subprocess.call(
                ["g++", "-g", "test/without_leak.cc", "-o",
                 "test/not_leaky.out"])
        self.assertFalse(uut.is_memleak("test/not_leaky.out"))

    def test_is_poor_style(self):
        """The tests should be able to run cpplint.py on files."""
        self.assertEqual(1, uut.is_poor_style("test/with_leak.cc"))
        self.assertEqual(0, uut.is_poor_style("test/without_leak.cc"))
