#!/usr/bin/env python2
# This program was developed and tested using python2.7.

import argparse
import os
import sys
import subprocess
from utils.color import cprint, cstr

def make_sure_hg_is_configured():
    f = os.path.join(os.path.expanduser('~'), '.hgrc')
    if not os.path.isfile(f):
        cprint("You do not have a ~/.hgrc file. Do you want "
               "a basic mercurial configuration file to be "
               "created for you? ")
        if raw_input().lower().startswith('y'):
            hgrc = "[ui]\nusername = {0}".format(os.environ["USER"])
            cprint("Executing the following command:")
            cprint(color="red",
                   msg='  $ echo >> ~/.hgrc "{0}"'.format(hgrc))
            os.system('echo >> ~/.hgrc "{0}"'.format(hgrc))


def path_to_labs_folder():
    """Finds the users path to the folder labs.

    :return: A path string or None.

    """
    path, f = os.path.split(os.path.realpath(os.path.curdir))
    while True:
        if not f:
            return False
        if f == "labs":
            return path
        else:
            path, f = os.path.split(path)


def discover_lab():
    """Identifies the lab number.

    This uses the current working directory. It looks for a sub-
    directory that starts with "lab".

    :return: The lab number.

    """
    path, f = os.path.split(os.path.realpath(os.path.curdir))
    while True:
        if not f:
            return False
        if f.startswith("lab") and not f == "labs":
            return int(f.lstrip('lab'))
        else:
            path, f = os.path.split(path)


def get_lab_main(lab_number=None):
    """Identifies and returns the main function for the correct lab.

    :type return: function object

    """
    path = path_to_labs_folder()
    if not path:
        cprint("You do not appear to be in a lab directory. Exiting.")
        raise Exception(cstr(color='red', msg="No lab found."))

    if not lab_number:
        lab_number = discover_lab()

    if lab_number == 2:
        from lab_controllers.lab2_controller.lab2 import main
    else:
        return False
        """
        raise Exception(
                cstr(color="red",
                     msg="Lab ({0}) is not recognized.".format(lab_number)))
        """
    return main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An assistance program for "
                                                 "homework and labs.")
    parser.add_argument("-o", "--overview", action="store_true",
                        help="Print the overview information for the lab.")
    parser.add_argument("-i", "--info", action="store_true",
                        help="Print the lab instructions for the current "
                             "activity.")
    parser.add_argument("-p", "--progress", action="store_true",
                        help="Display your progress.")
    parser.add_argument("-c", "--check", action="store_true",
                        help="Test your progress for this phase of the lab.")
    parser.add_argument("-s", "--start", type=int,
                        help="Starts the lab with the specified number. The "
                             "current directory must be .../labs and "
                             "the lab directory .../labs/labN must "
                             "either be empty or non-existant. Example: "
                             "'labs --start=2' will start lab2.")

    args = parser.parse_args()

    arg_flag = False
    for arg in [args.overview, args.info, args.progress, args.check,
                args.start]:
        if arg:
            arg_flag = True

    make_sure_hg_is_configured()

    if not path_to_labs_folder():
        if os.path.exists(os.path.join('.', "labs")):
            cprint("The folder 'labs' exists in the current working "
                   "directory. Move to this directory using the following command:")
            cprint(color="red", msg="  $ cd labs")
        else:
            cprint("Do you wish to create the labs directory? (y/n)")
            choice = raw_input()
            if choice.lower().startswith('y'):
                cprint("Executing the following command:")
                cprint(color="red", msg="  $ mkdir labs")
                subprocess.check_call(['mkdir', 'labs'])
                cprint("Change directory into labs and execute "
                       "the following to start a lab:")
                cprint(color="red",
                       msg="  $ lab_tools --start=[labnumber]")
        sys.exit(0)
    else:
        lab_main = get_lab_main(args.start)

    if lab_main:
        if arg_flag:
            lab_main(args.overview, args.info, args.progress, args.check,
                     args.start)
        else:
            parser.print_help()
    else:
        if arg_flag or path_to_labs_folder():
            parser.print_help()
            if path_to_labs_folder():
                cprint("No lab found. Either change directory to a lab "
                       "folder or start a new lab.")
        else:
            cprint("Do you wish to create labs in the current "
                   "directory? (y/n)")
            choice = raw_input()
            if choice.lower().startswith('y'):
                cprint("Executing the following command:")
                cprint(color="red", msg="  $ mkdir labs")
                subprocess.check_call(['mkdir', 'labs'])
                cprint("You will need to change directory to the new folder "
                       "before starting/continuing a lab.")

