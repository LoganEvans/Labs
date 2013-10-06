import inspect
import sys
import re
from binlab_error import BinlabError

DISPLAY = True

def toggle_display(set_value=None):
    """Toggles automatic display of operations.

    This exists so that a user who has used "from binlab import *" can still
    modify the value."""

    global DISPLAY
    if set_value:
        DISPLAY = set_value
    else:
        DISPLAY = not DISPLAY


def displayable(func):
    return my_coerce(_display(func))
    #return _display(my_coerce(func))


def my_coerce(func):
    def decorated(self, *other):
        if other:
            return func(self, self.__class__(other[0], bitlen=self.bitlen))
        else:
            return func(self)

    # Without this, the func_name would show up as decorated. However, in
    # the _display decorator, we check for the function name.
    decorated.func_name = func.func_name
    return decorated


def _print_unary_op(operand, func_symbol, retval):
    fmt_str = ['']
    fmt_str += ['-' * 100]
    fmt_str += ["| {0:<16} |{1:>18} |{2:>18} |{3:>18} |{4:>18} |".format(
            'Encoding', 'Binary Value', 'Integer Value', 'Hexadecimal Value',
            'Octal Value')]
    fmt_str += ["|" + "-" * 18 + "|" + ("-" * 19 + "|") * 4]
    fmt_str += ["| {a[type_of]:<16} |"
                "{func_symbol:>3}{a[bin_of]:>15} |"
                "{func_symbol:>3}{a[int_of]:>15} |"
                "{func_symbol:>3}{a[hex_of]:>15} |"
                "{func_symbol:>3}{a[oct_of]:>15} |"]
    fmt_str += ["|" + "-" * 18 + "|" + ("-" * 19 + "|") * 4]
    fmt_str += ["| {res[type_of]:<16} |{res[bin_of]:>18} |{res[int_of]:>18} |"
                "{res[hex_of]:>18} |{res[oct_of]:>18} |"]
    fmt_str += ['-' * 100]

    fmt_str = '\n'.join(fmt_str)
    a = {}
    res = {}

    for dict_, operand in [[a, operand], [res, retval]]:
        dict_['type_of'] = operand.obj_type()
        dict_['bin_of'] = str(operand)
        dict_['int_of'] = operand.val
        dict_['hex_of'] = hex(operand.val)
        dict_['oct_of'] = oct(operand.val)

    print_str = fmt_str.format(a=a, res=res, func_symbol=func_symbol) + "\n"
    sys.stdout.write(print_str)

def _print_binary_op(op_a, op_b, func_symbol, retval):
    fmt_str = ['']
    fmt_str += ['-' * 100]
    fmt_str += ["| {0:<16} |{1:>18} |{2:>18} |{3:>18} |{4:>18} |".format(
            'Encoding', 'Binary Value', 'Integer Value', 'Hexadecimal Value',
            'Octal Value')]
    fmt_str += ["|" + "-" * 18 + "|" + ("-" * 19 + "|") * 4]
    fmt_str += ["| {a[type_of]:<16} |{a[bin_of]:>18} |{a[int_of]:>18} |"
                "{a[hex_of]:>18} |{a[oct_of]:>18} |"]
    fmt_str += ["| {b[type_of]:<16} |"
                "{func_symbol:>2}{b[bin_of]:>16} |"
                "{func_symbol:>2}{b[int_of]:>16} |"
                "{func_symbol:>2}{b[hex_of]:>16} |"
                "{func_symbol:>2}{b[oct_of]:>16} |"]
    fmt_str += ["|" + "-" * 18 + "|" + ("-" * 19 + "|") * 4]
    fmt_str += ["| {res[type_of]:<16} |{res[bin_of]:>18} |{res[int_of]:>18} |"
                "{res[hex_of]:>18} |{res[oct_of]:>18} |"]
    fmt_str += ['-' * 100]
    fmt_str = '\n'.join(fmt_str)

    a = {}
    b = {}
    res = {}

    for dict_, operand in [[a, op_a], [b, op_b], [res, retval]]:
        dict_['type_of'] = operand.obj_type()
        dict_['bin_of'] = str(operand)
        dict_['int_of'] = operand.val
        dict_['hex_of'] = hex(operand.val)
        dict_['oct_of'] = oct(operand.val)

    print_str = fmt_str.format(a=a, b=b, res=res, func_symbol=func_symbol) + "\n"
    sys.stdout.write(print_str)


def _display(func):
    """This is a decorator for binary operations.

    It will display the
    operands in their native binary, decimal, and hexadecimal. It will show
    the results, and the operation performed."""

    def decorated(self, *other):
        """self is expected because this will only decorate methods. other,
        however, might or might not exist."""

        retval = func(self, *other)
        # Well... this is a pretty terrible solution... I'm making certain that
        # the module that initiated this call is NOT binlab.py. So, this makes
        # the assumption that all paths that should be printed are short.

        if not DISPLAY or re.search('binlab.py', inspect.stack()[2][1]):
            return retval

        op = func.func_name
        if not op:
            raise BinlabError('"{0}" is not a recognized Binlab '
                              'function.'.format(func.func_name))
        else:
            if op in self._unary_func_names:
                _print_unary_op(self, self._unary_func_names[func.func_name],
                                retval)
            elif op in self._binary_func_names:
                _print_binary_op(self, other[0],
                                 self._binary_func_names[func.func_name],
                                 retval)
            else:
                raise BinlabError('"{0}" is not a recognized Binlab '
                                  'operation.'.format(op))

        return retval

    return decorated


