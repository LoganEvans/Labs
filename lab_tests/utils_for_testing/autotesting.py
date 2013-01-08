import re
import os
import subprocess
import shlex
from utils.env_settings import TESTS_DIR

def get_outstreams(*args):
    """Returns [stdout, stderr, return code] of the input command.

    This command will not use a shell.

    """
    ret = subprocess.Popen(*args, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout_, stderr_ = ret.communicate()
    retcode = ret.returncode
    return [stdout_, stderr_, retcode]


def get_stdout(*args):
    """Returns the stdout result of a command."""
    return get_outstreams(*args)[0]


def is_memleak(command):
    """Checks if the compiled program has a memory leak."""
    # Make sure the log is empty.
    subprocess.call(["touch", "data/valgrind_errors.log"])
    subprocess.call(["rm", "data/valgrind_errors.log"])
    subprocess.call(["touch", "data/valgrind_errors.log"])
    subprocess.call(["valgrind", "-q", "--leak-check=full",
                     "--log-file=data/valgrind_errors.log"] +
                     shlex.split(command))
    if get_stdout(["cat", "data/valgrind_errors.log"]):
        return True
    return False


def is_poor_style(source_cpp):
    """Returns the number of style errors found in the source code.

    The copyright and streams errors are filtered out of the test.

    """
    message = get_outstreams([
            "python2",
            os.path.join(TESTS_DIR, "utils_for_testing", "cpplint.py"),
            "--filter=-legal/copyright,-readability/streams",
            source_cpp])
    stderr_message = message[1]
    num_errors = re.search(r"Total errors found: (\d+)", stderr_message)
    if num_errors:
        return int(num_errors.group(1))
    return -1

