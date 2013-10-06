from __future__ import print_function
import cPickle as pickle
import glob
import os
import subprocess
import sys
from utils.env_settings import SOURCE_DIR, TESTS_DIR, BOILERPLATES_DIR
from utils.color import cprint

def labdir():
    ret = os.path.realpath(os.path.curdir)
    while True:
        updir, f = os.path.split(ret)
        if not f:
            raise Exception("No lab found.")
        if f.startswith('lab'):
            return ret
        ret = updir


def set_progress(progress):
    assert isinstance(progress, int)
    data_dir = os.path.join(labdir(), "data")
    if not os.path.exists(data_dir):
        cprint("Creating the 'data' directory using the following command:")
        cprint(color="red", msg="  $ mkdir {0}".format(data_dir))
        subprocess.check_call(['mkdir', data_dir])
    with open(os.path.join(data_dir, "lab2_progress.pickle"), "wb") as outfile:
        pickle.dump(progress, outfile)


def get_progress():
    try:
        with open(os.path.join(labdir(), "data", "lab2_progress.pickle"), "rb") as infile:
            return pickle.load(infile)
    except IOError:
        return None


def main(overview, info, progress, check, start):
    pkl = None
    if start:
        if "lab2" not in glob.glob("*"):
            cprint("Executing the following command:")
            cprint(color="red",
                   msg="  $ cp -r {boiler}/lab2_boilerplate lab2".format(boiler=BOILERPLATES_DIR))
            subprocess.check_call(['cp', '-r',
                                   os.path.join(BOILERPLATES_DIR, 'lab2_boilerplate'),
                                   'lab2'])
        else:
            cprint("The folder lab2 already exists.")
        cprint("Change directory into the new folder to work on the lab.")
        sys.exit(0)

    with open(os.path.join(SOURCE_DIR, "lab_controllers", "lab2_controller",
                           "lab2_instructions.pickle"), 'rb') as infile:
        pkl = pickle.load(infile)

    if get_progress() == 4 and (info or progress or check):
        cprint("All activities completed.")
        cprint("Generating submission...")
        subprocess.check_call(['make', 'submit'])
        cprint(color="green",
               msg="Congratulations! You are done with the lab.")
        exit()

    if overview:
        print(pkl["overview"])
    if info:
        print(pkl["activities"][get_progress()])
    if check:
        testmap = {0: 'test_activity0.py',
                   1: 'test_activity1.py',
                   2: 'test_activity2.py',
                   3: 'test_activity3.py'}
        progress = get_progress()
        test_to_perform = os.path.join(TESTS_DIR, "lab2_tests", testmap[progress])
        cprint("The following command runs these tests:")
        cprint(color="red",
               msg="  $ nosetests {test_to_perform} -sv".format(
                                                test_to_perform=test_to_perform))
        cprint("--------------------------------------")
        try:
            subprocess.check_call(['nosetests',
                                   test_to_perform, '--nocapture',
                                   '--verbose', '--rednose'])
            set_progress(get_progress() + 1)
        except subprocess.CalledProcessError:
            cprint(color="red", msg="------------------------------------")
            cprint(color="red",
                   msg="One or more requirements were not met.")
    if progress or check:
        print()
        cprint("You are currently on Activity {0}".format(get_progress()),
               color="red")
        cprint('Execute "lab_tools --check" to check your progress.')
        cprint('Execute "lab_tools --info" for a list of your '
               'current tasks.')
        print()

