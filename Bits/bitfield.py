"""
Jacob Rammer
Bitwise project
"""

import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

"""
A bit field is a range of binary digits within an
unsigned integer.   Bit 0 is the low-order bit,
with value 1 = 2^0.  Bit 31 is the high-order bit, 
with value 2^31. 

A bitfield object is an aid to encoding and decoding 
instructions by packing and unpacking parts of the 
instruction in different fields within individual 
instruction words. 
"""

# --------------
# Constants
# --------------

WORD_SIZE = 32  # represents bits (x32)


class BitField(object):
    """
    A bitfield object extracts specified bitfields from an integer.
    """

    def __init__(self, from_bit: int, to_bit: int) -> None:
        """
        Tool for extracting bits from_bit ... to_bit, where 0 is the low-order
        bit and 31 is the high-order bit of an unsigned 32-bit integer. For example, 
        the low-order 4 bits could be represented bit from_bit=0, to_bit = 3.
        """

        assert 0 <= from_bit < WORD_SIZE
        assert from_bit <= to_bit <= WORD_SIZE

        self.from_bit = from_bit
        self.to_bit = to_bit
        self.bit_width = self.to_bit - self.from_bit + 1

        self.mask = 0
        for i in range(self.bit_width):
            self.mask = (self.mask << 1) | 1

    def extract(self, word: int) -> int:
        """
        Extract the bitfield and return it in the low-order bits. 
        For example, if we are extracting bits 3..5, the result will
        be an integer between 0 and 7 (0b000 to 0b111)
        """

        return (word >> self.bit_width) & self.mask