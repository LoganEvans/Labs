import inspect
import pickle
import os
import sys

CUR_FILE = os.path.abspath(inspect.getfile(inspect.currentframe()))
CUR_DIR = os.path.split(CUR_FILE)[0]
CONTROLLER_DIR = os.path.split(CUR_DIR)[0]
SOURCE_DIR = os.path.split(CONTROLLER_DIR)[0]
sys.path.append(SOURCE_DIR)

from utils.color import cstr


### instructions
instructions = [cstr("\nInstructions:", color="green")]
instructions += [cstr("In order to check your progress, type:")]
instructions += [cstr("  $ lab_tools --progress", color="red")]
instructions += [cstr("In order to run tests on this activity, type:")]
instructions += [cstr("  $ lab_tools --check", color="red")]
instructions += [cstr(color="cyan",
msg="""\
Note: The lab_tools program will not record forward progress unless your
      program passes all tests executed with the --check flag""")]
instructions = '\n'.join(instructions)

### overview
overview = [cstr("\nOverview:", color="green")]
overview += [cstr(
"""Using the command line to pass arguments to programs is very common in the
unix world. Long before there were graphical user interface (gui) based
programs, the command line was used to specify program options. Consider the
following simple examples:
""")]
overview += [cstr(msg="  $ ls -l", color="red")]
overview += [cstr(msg="  $ make -f app.make\n", color="red")]
overview += [cstr(
"""In the first command, the -l (letter ell) option requests that the long form
of a directory listing be used. In the second, the -f app.make option tells
make to read the rules defined in app.make. We will learn more about make
later.""")]
overview += [cstr("\nHandling Commandline Arguments:", color="green")]
overview += [cstr(
"""The standard prototype for the main function in C/C++ (and a number of other
programming languages) in the Unix environment is:""")]
overview += [cstr("\nint main(int argc, char *argv[]);\n", color="magenta")]
overview += [cstr("or")]
overview += [cstr("\nint main(int argc, char **argv);", color="magenta")]
overview += [cstr(
"""The first argument, argc, holds the number of items in the argv array. Note
that argv contains character strings (an array of characters). This requires
numbers entered on the command line to be converted from a character string to
the necessary numerical data type.""")]
overview = '\n'.join(overview)

### activities
activities = []

####### activity1
activity0 = [cstr(color="green", msg="\nWelcome to Lab 2.")]
activity0 += [cstr(
"""Before you get started on the lab, you should create a new repository using
the following commands:""")]
activity0 += [cstr(color="red", msg="  $ hg init")]
activity0 += [cstr(color="red", msg="  $ hg addremove")]
activity0 += [cstr(color="red", msg='  $ hg com -m "Initial commit."')]
activity0 += [cstr(
"""Once this is done, check your progress with the following command:""")]
activity0 += [cstr(color="red", msg="  $ lab_tools --check")]
activities.append('\n'.join(activity0))

####### activity1
activity1 = [cstr("\nActivty 1:", color="green")]
activity1 += [cstr(
"""Write a small program (ShowArgs) to print out all arguments given to a
program.

Example output:""")]
activity1 += [cstr(color="red", msg="""  $ ./ShowArgs foo bar baz
./ShowArgs
foo
bar
baz
""")]
activity1 += [cstr("""
 * Use the provided files.
   * A file named "Makefile" is provided.
   * Place all prototypes in "definitions_lab2.h"
   * Place all definitions for these prototypes in "utilities_lab2.cc"
   * Place your main() function in "main_lab2.cc"
 * Your program should print one commandline argument per line.
 * From the commandline, use the following commands to backup your work:""")]
activity1 += [cstr(color="red", msg="  $ hg addremove  # This tells mercurial "
                                    "to track any new files and untrack "
                                    "deleted ones.")]
activity1 += [cstr(color="red", msg='  $ hg com -m "This commit message '
                                    'describes what the changeset does using '
                                    'present tense."')]
activity1 += [cstr(" * Execute the following command to build the ShowArgs "
                   "executable:")]
activity1 += [cstr(color="red", msg="  $ make activity1")]
activity1 += [cstr(" * Execute the following command to check if all tasks "
                   "for this activity are complete:")]
activity1 += [cstr(color="red", msg="  $ lab_tools --check")]
activities.append('\n'.join(activity1))

####### activity2
activity2 = [cstr("\nActivity 2:", color="green")]
activity2 += [cstr("""\
Revise your program to add error handling code. The program should require at
least three command line arguments.
 * The executable will be named Act2. Use "make activity2" to make the project.
 * If too few arguments have been supplied, use the code "exit(17)" to exit
   the program.
 * This is an example of how your program should behave:""")]
activity2 += [cstr(color="red", msg="""\
  $ echo 'Hello, world!'
Hello, world!
  $ echo $?
0
  $ ./Act2 foo bar baz
  $ echo $?
0
  $ ./Act2 spam eggs
  $ echo $?
17
""")]
activity2 += [cstr(msg="""\
 * From the commandline, use the following commands to backup your work:""")]
activity2 += [cstr(color="red", msg="  $ hg addremove  # This tells mercurial "
                                    "to track any new files and untrack "
                                    "deleted ones.")]
activity2 += [cstr(color="red", msg='  $ hg com -m "This commit message '
                                    'describes what the changeset does using '
                                    'present tense."')]
activity2 += [cstr(" * Execute the following command to build the ShowArgs "
                   "executable:")]
activity2 += [cstr(color="red", msg="  $ make activity2")]
activity2 += [cstr(" * Execute the following command to check if all tasks "
                   "for this activity are complete:")]
activity2 += [cstr(color="red", msg="  $ lab_tools --check")]
activities.append('\n'.join(activity2))

####### activity3
activity3 = [cstr("\nActivity 3:", color="green")]
activity3 += [cstr("""\
Modify your program so that it handles simple arithmetic computations.
E.g.:""")]
activity3 += [cstr("  $ calc 2 * 3  #=> 6", color="red")]
activity3 += [cstr("""\
 * The executable will be named calc. Use "make activity3" to make the project.
 * The executable should accept exactly 3 arguments. Return '17' if too few
   or too many arguments are supplied.
 * The following operators must be supported: +, -, *, /, %
 * Use the atof function from stdlib.h for the following operators: +, -, *, /
   The prototype for atof is: double atof(const char *str);
 * Use the atoi function form stdlib.h for the following operator: %
   The prototype for atoi is: int atoi(const char *str);
 * From the commandline, use the following commands to backup your work:""")]
activity3 += [cstr(color="red", msg="  $ hg addremove  # This tells mercurial "
                                    "to track any new files and untrack "
                                    "deleted ones.")]
activity3 += [cstr(color="red", msg='  $ hg com -m "This commit message '
                                    'describes what the changeset does using '
                                    'present tense."')]
activity3 += [cstr(" * Execute the following command to build the calc "
                   "executable:")]
activity3 += [cstr(color="red", msg="  $ make activity3")]
activity3 += [cstr(" * Execute the following command to check if all tasks "
                   "for this activity are complete:")]
activity3 += [cstr(color="red", msg="  $ lab_tools --check")]

activities.append('\n'.join(activity3))

with open('lab2_instructions.pickle', 'wb') as outfile:
    to_dump = {'overview': overview,
               'instructions': instructions,
               'activities': activities}
    pickle.dump(to_dump, outfile)
