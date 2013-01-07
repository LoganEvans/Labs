from base_binary import BaseBinary

class ComplimentBinary(BaseBinary):
    """Represents binary numbers using a 2's compliment scheme."""
    def __init__(self, val=0, bitlen=None):
        # Not set as default because of parse vs execute time issue
        BaseBinary.__init__(self, val=val, bitlen=bitlen)

    def _add_one(self, bitlist, index=None):
        if index is None:  # index can be 0
            index = len(bitlist) - 1
        if bitlist[index] == '0':
            bitlist[index] = '1'
        else:
            bitlist[index] = '0'
            if index:  # i.e. index != 0
                self._add_one(bitlist, index - 1)

    def __str__(self):
        if self.sign == '0':
            rep = bin(self.val).lstrip('0b')
        else:
            rep = bin(self.val).lstrip('-0b')
            rep = "{rep:0>{self.bitlen}}".format(rep=rep, self=self)
            bits = []
            for bit in rep:
                bits.append('1' if bit == '0' else '0')
            self._add_one(bits)
            rep = ''.join(bits)

        return "{rep:{self.sign}>{self.bitlen}}".format(rep=rep, self=self)

    def _from_str_to_int(self, str_rep):
        bits = []
        for bit in str_rep:
            bits.append(bit)
        negative = False
        if bits[0] == '1':
            negative = True

            # Flip all bits
            for i, _ in enumerate(bits):
                bits[i] = '0' if bits[i] == '1' else '1'

            self._add_one(bits)
        bits = ''.join(bits)
        val = int(bits, 2)
        if negative:
            val = -val

        return val


class SignedMagnitude(BaseBinary):
    """Represents binary numbers where the most significant bit (far left)
    represents sign, and the remaining bits represent the magnitude.

    """
    def __init__(self, val=0, bitlen=None):
        BaseBinary.__init__(self, val=val, bitlen=bitlen)

    def __str__(self):
        if self.sign == '0':
            rep = bin(self.val).lstrip('0b')[-self.bitlen + 1:]
        else:
            rep = bin(self.val).lstrip('-0b')[-self.bitlen + 1:]

        return "{self.sign}{rep:0>{bitlen}}".format(rep=rep, self=self,
                                                    bitlen=self.bitlen - 1)

    def _from_str_to_int(self, str_rep):
        if 'b' in str_rep:
            val = int(str_rep, 2)
        else:
            val = int(str_rep[1:], 2)
            if str_rep[0] == '1':
                val = -val
        return val


class UnsignedBinary(BaseBinary):
    """Represents binary numbers using unsigned magnitude."""
    def __init__(self, val=0, bitlen=None):
        if isinstance(val, int):
            msg = "UnsignedBinary cannot recognize this negative number: {0}".format(val)
            assert val >= 0, msg
        BaseBinary.__init__(self, val=val, bitlen=bitlen)

    def __str__(self):
        rep = bin(self.val).lstrip('0b')
        return "{rep:0>{bitlen}}".format(rep=rep, self=self,
                                         bitlen=self.bitlen)

    def _from_str_to_int(self, str_rep):
        return int(str_rep, 2)


class GrayCode(BaseBinary):
    """Represents binary numbers using gray code."""
    def __init__(self, val=0, bitlen=None):
        if isinstance(val, int):
            msg = "UnsignedBinary cannot recognize this negative number: {0}".format(val)
            assert val >= 0, msg
        BaseBinary.__init__(self, val=val, bitlen=bitlen)

    def __str__(self):
        ref = '0' + str(UnsignedBinary(self.val, bitlen=self.bitlen))
        new_str = []
        for i in range(1, len(ref)):
            new_str.insert(0, str(int(ref[-i]) ^ int(ref[-i - 1])))
        return ''.join(new_str)

    def _from_str_to_int(self, str_rep):
        if 'b' in str_rep:
            return 0
        my_xor = lambda a, b: str(int(a) ^ int(b))
        rep = [c for c in str_rep]
        shifted_rep = [c for c in str_rep]
        for i in range(len(str_rep) - 1, 0, -1):
            shifted_rep.insert(0, '0')
            for i in range(len(rep)):
                rep[i] = my_xor(rep[i], shifted_rep[i])
        return int(UnsignedBinary(''.join(rep), bitlen=len(str_rep)))

