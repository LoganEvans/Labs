from abc import ABCMeta, abstractmethod, abstractproperty
from display import displayable
from binlab_error import BinlabError
import re

DEFAULTBITS = 8

class BaseBinary(object):
    """This base class defines all of the arithmatic operations for the
    inheriting classes.

    This class needs to define operations for quite a number of
    operators. Each of these operators must first coerce the operands to
    a common type, then must be able to display the operations, and then must
    return the correct values. For all of them, the operations are the same:

    1) Coerce the second operand into the datatype of the first.
    2) Perform the operation using obj1.val OP obj2.val
    3) Report the display type, operators, and return value to a display
       function.
    4) Return the correct value.

    """
    # Note: I'm not metaclassing because the syntax is different
    # between python2 and python3.
    #
    # This could plausibly be done with some metaclass shenatigans. First, it
    # would probably be pragmatic to remove the ABCMeta definition and instead
    # use a Python 2.5 style abstract base class. Second, we would define a
    # metaclass that automatically applies 2 decorators to the methods named
    # in the _(\w+)_func_names lists below. The first would coerce the second
    # argument into the datatype of the first (using bincast), and the second
    # decorator would decorate the operator with the appropriate _print function.
    #
    # Instead, I'm going to manually apply these decorators, because that
    # syntax should be the same for python2 and python3.

    __metaclass__ = ABCMeta

    # These names are used to switch on the correct display mechanism.
    _unary_func_names = {'__neg__' : '-', '__pos__' : '+',
                         '__abs__' : 'abs', '__invert__' : '~'}
    # xnor doesn't really exist, but it is discussed a lot in digital logic
    # classes.
    _binary_func_names = {'__add__' : '+', '__sub__' : '-', '__mul__' : '*',
                          '__and__' : '&', '__xor__' : '^', '__or__' : '|',
                          'xnor' : '!^'}
    #  '__lshift__', '__rshift__', 
    _comparison_func_names = ['__cmp__']
    #['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__']
    _boolean_func_names = ['__nonzero__']


    @abstractmethod
    def __init__(self, val=0, bitlen=None):
        """
        @param val (int or str)
            If str, use base 10.
        @param bitlen (int)
            The number of bitlen to use in the representation.
        @param encoding (str)
            Use one of ['compliment', 'signed', 'invert']

        """

        if isinstance(val, int):
            self.val = val
        elif isinstance(val, str):
            self.val = self._from_str_to_int(val)
        elif isinstance(val, BaseBinary):
            self.val = val.val
        else:
            raise BinlabError()

        # Not set as default because of parse vs execute time issue
        self.bitlen = bitlen or DEFAULTBITS

    @abstractmethod
    def _from_str_to_int(self, str_rep):
        """
        This does not set the self.bitlen attribute.
        """
        pass

    @property
    def sign(self):
        return '0' if self.val >= 0 else '1'

    @property
    def bitlen(self):
        """The alternative to this is to import abc and then set __metaclass__
        to abcmeta, or something like that."""

        return self._bitlen

    @bitlen.setter
    def bitlen(self, bitlen):
        """This method  is the reason for the properties. When we set the
        bitlen, we want to automatically truncate or extend the binary
        number.

        """
        self._bitlen = bitlen
        #if len(self.__str__()) != bitlen:
        self._truncate()

    @bitlen.deleter
    def bitlen(self):
        del self._bitlen

    def obj_type(self):
        return re.search(r"\.(\w+)'>$", str(type(self))).group(1)

    def _truncate(self):
        """Should be called ONLY from bitlen.setter. This takes the rightmost
        bitlen and creates a new object using these. It then sets the self.val
        to this new value."""
        self.val = self._from_str_to_int(str(self)[-self.bitlen:])

    def _extend(self):
        """Called by bitlen.setter after the bitlen have been lengthened."""
        pass

    @abstractmethod
    def __str__(self):
        str_val = []
        str_val += ["val (base 10): {self.val}"]
        str_val += ["bitlen: {self.bitlen}"]
        str_val = '\n'.join(str_val)
        return str_val.format(self=self)

    def invert(self):
        """Returns the invert.

        I would use (self ^ 0), but I don't have a 0 or 1 easily defined."""

        new_str = []
        for c in str(self):
            new_str.append('1' if str(c) == '0' else '0')

        new_str = ''.join(new_str)
        return self.__class__(new_str)

    def __int__(self):
        return self.val

    @displayable
    def __neg__(self):
        return self.__class__(val= - int(self), bitlen=self.bitlen)

    @displayable
    def __pos__(self):
        return self.__class__(val=int(self), bitlen=self.bitlen)

    @displayable
    def __abs__(self):
        return self.__class__(val=abs(int(self)), bitlen=self.bitlen)

    @displayable
    def __invert__(self):
        new_rep = ''.join(['0' if x == '1' else '1' for x in str(self)])
        return self.__class__(val=new_rep, bitlen=self.bitlen)

    @displayable
    def __add__(self, other):
        # The int branch is used in a situation where I use (self + 1) to
        # find the negative representation of some numbers. It's nice to be
        # able to increment easily. I don't think that an int needs be
        # supported in any other operation, except maybe __sub__?
        if type(other) == int:
            op_b = self.__class__(val=other)
        else:
            op_b = self.__class__(val=other, bitlen=self.bitlen)
        retval = self.__class__(val=int(self) + int(op_b),
                                bitlen=self.bitlen)
        return retval

    @displayable
    def __sub__(self, other):
        op_b = self.__class__(val=other, bitlen=self.bitlen)
        retval = self.__class__(val=int(self) - int(op_b),
                                bitlen=self.bitlen)
        return retval

    @displayable
    def __mul__(self, other):
        op_b = self.__class__(val=other, bitlen=self.bitlen)
        # Omitting the bitlen param and using a str for val so that auto
        # bitlen sizing will take place.
        retval = self.__class__(val=int(self) * int(op_b))
        return retval

    # TODO
    def __lshift__(self, other):
        pass

    # TODO
    def __rshift__(self, other):
        pass

    @displayable
    def __and__(self, other):
        new_str = []
        for i in range(len(str(self))):
            if str(self)[i] == '1' and str(other)[i] == '1':
                new_str.append('1')
            else:
                new_str.append('0')

        new_str = ''.join(new_str)
        return self.__class__(new_str)

    @displayable
    def __xor__(self, other):
        new_str = []
        for i in range(len(str(self))):
            if str(self)[i] == str(other)[i]:
                new_str.append('0')
            else:
                new_str.append('1')

        new_str = ''.join(new_str)
        return self.__class__(new_str)

    @displayable
    def __or__(self, other):
        new_str = []
        for i in range(len(str(self))):
            if str(self)[i] == '1' or str(other)[i] == '1':
                new_str.append('1')
            else:
                new_str.append('0')

        new_str = ''.join(new_str)
        return self.__class__(new_str)

    def xnor(self, other):
        return ~ (self ^ other)

    def __cmp__(self, other):
        return int(self) - int(other)


