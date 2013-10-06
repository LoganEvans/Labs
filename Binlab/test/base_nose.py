from .. import base_binary
from ..binary import *
import unittest
import sys
from abc import ABCMeta, abstractmethod

class BaseNose(object):
    __metaclass__ = ABCMeta
    restore_DEFAULTBITS = base_binary.DEFAULTBITS

    @abstractmethod
    def setUp(self):
        """This allows other tests to change the Unit Under Test."""
        # self.UUT = ComplimentBinary

    def tearDown(self):
        base_binary.DEFAULTBITS = self.restore_DEFAULTBITS

    def test_equal(self, range_low=None, range_high=None):
        """Equality should work correctly."""
        bitlen = self.UUT().bitlen

        if range_low is None:
            range_low = int(-(2 ** (bitlen - 1)))

        if range_high is None:
            range_high = int(2 ** (bitlen - 1) - 1)

        for i in range(range_low, range_high):
            uut = self.UUT(i)
            self.assertTrue(i == uut, "{0} == {1} ; bitlen: {2} obj_type: {3}".format(
                                                    i, uut, bitlen, self.UUT().obj_type))

    def binary_operation(self, op_name='__add__', test_arr=None):
        """The binary operations should work correctly.

        :param op_name:
            The dictionary key to the int attribute that will be
            used for the test. E.g. '__add__' will leverage the + mechanic.
        :param test_arr:
            All pairwise combinations of values in test_arr will
            be used in the test.

        """
        if test_arr is None:
            test_arr = [-63, -1, 0, 1, 63]

        for i in test_arr:
            for j in test_arr:
                a = self.UUT(i)
                b = self.UUT(j)

                op_int = int.__dict__[op_name](i, j)
                op_UUT = self.UUT(i).__getattribute__(op_name)(j).__int__()
                self.assertEqual(op_int, op_UUT,
                                 "Op {0} failed. {1} != {2}".format(op_name, op_int, op_UUT))
                self.assertEqual(i < j, a < j)
                self.assertEqual(i < j, i < b)
                self.assertEqual(i > j, a > b)
                self.assertEqual(i > j, a > j)
                self.assertEqual(i > j, i > b)

    def test_binary_operations(self, test_arr=None, op_names=['__add__', '__sub__']):
        if test_arr is None:
            test_arr = [-63, -1, 0, 1, 63]

        for test in op_names:
            self.binary_operation(op_name=test, test_arr=test_arr)

        self.binary_operation(op_name='__mul__', test_arr=[0, 1, 4, 10])

    def test_DEFAULTBITS(self, range_low=None, range_high=None, test_arr=None, no_subtract=False):
        """Tests should pass if the bit lengths are different."""
        # Note: higher values for DEFAULTBITS, such as 29, managed to lock my
        # computer. At 30, I got a MemoryError.
        for i in range(9, 16, 3):
            base_binary.DEFAULTBITS = i
            self.test_equal(range_low, range_high)
            self.binary_operation('__add__', test_arr=test_arr)
            if not no_subtract:
                self.binary_operation('__sub__', test_arr=test_arr)

    def test_bitlen(self):
        """It should allow custom bit length."""
        val = self.UUT(val=5, bitlen=4)
        self.assertEqual(val.bitlen, 4)

    def test_truncate(self):
        """It should truncate the bitlen."""
        val = self.UUT(val=5, bitlen=2)
        self.assertEqual(val.bitlen, 2)
        self.assertTrue(val == 1)

