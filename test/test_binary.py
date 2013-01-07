from base_nose import BaseNose
from ..binary import *
from unittest import TestCase


class ComplimentBinaryTest(BaseNose, TestCase):
    def setUp(self):
        self.UUT = ComplimentBinary


class SignedMagnitudeTest(BaseNose, TestCase):
    """All tests should work if the unit we are testing is SignedMagnitude."""
    def setUp(self):
        self.UUT = SignedMagnitude

    def test_equal(self, range_low=None, range_high=None):
        """SignedMagnitude's equality should work for its range."""
        bitlen = self.UUT().bitlen
        BaseNose.test_equal(self, range_low=(int(2 ** (bitlen - 1)) - 1))


class UnsignedBinaryTest(BaseNose, TestCase):
    """All tests should work if the unit we are testing is UnsignedBinary."""
    def setUp(self):
        self.UUT = UnsignedBinary

    def test_equal(self, range_low=None, range_high=None):
        bitlen = self.UUT().bitlen
        BaseNose.test_equal(self, range_low=0, range_high=(2 ** bitlen) - 1)

    def test_DEFAULTBITS(self, range_low=None, range_high=None, test_arr=None):
        """Tests should pass if the bit lengths are different."""
        bitlen = self.UUT().bitlen
        range_high = 2 ** bitlen - 1
        BaseNose.test_DEFAULTBITS(self, range_low=0, range_high=range_high,
                                  test_arr=[0, 1, 2, 5, 60, 63],
                                  no_subtract=True)

    def test_binary_operations(self, test_arr=None, op_names=None):
        BaseNose.test_binary_operations(self, [0, 1, 2, 4, 7, 10, 63], op_names=['__add__'])

    def test_subtraction(self):
        """Subtraction should work when the result is possitive."""
        self.assertEqual(self.UUT(5) - self.UUT(3), 2)
        self.assertEqual(self.UUT(127) - self.UUT(0), 127)
        self.assertEqual(self.UUT(127) - self.UUT(127), 0)
        self.assertEqual(self.UUT(255) - self.UUT(255), 0)
        self.assertEqual(self.UUT(255) - self.UUT(1), 254)


class GrayCodeTest(UnsignedBinaryTest, TestCase):
    """All tests should work if the unit we are testing is GrayCode."""
    def setUp(self):
        self.UUT = GrayCode

    def test_conversion(self):
        val = self.UUT(10)
        for val in [0, 1, 2, 4, 39, 120, 255]:
            self.assertTrue(str(val).endswith(str(int(str(val)))))

