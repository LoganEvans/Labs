from __future__ import print_function
import unittest
import os
import sys
import subprocess
import glob
import env_settings
from lab_tests.utils_for_testing.autotesting import *
from utils.color import cprint, cstr


class TestActivity0(unittest.TestCase):
    def test_testing(self):
        """This test should always pass."""

    def test_repository(self):
        """All work should be backed up."""
        try:
            if subprocess.check_output(['hg', 'status']):
                self.fail("There are uncommitted changes.")
        except subprocess.CalledProcessError:
            fail_msg = [cstr("\nNo repository exists.")]
            fail_msg += [cstr("From the commandline, use the following commands to "
                              "backup your work:")]
            fail_msg += [cstr(color="red", msg="  $ hg init")]
            fail_msg += [cstr(color="red", msg="  $ hg addremove")]
            fail_msg += [cstr(color="red", msg='  $ hg com -m "Initial commit."')]
            fail_msg = "\n".join(fail_msg)
            self.fail(fail_msg)


