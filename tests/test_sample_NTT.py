"""
Test file.
"""

# 

import unittest
from secrets import token_bytes
from utils.functions import _sample_ntt

class Test_Sample_ntt(unittest.TestCase):
    """
    Tests for sample_ntt
    """

    def test_improper_length(self):
        """
        Should raise ValueError if the length of the input is less than 32 bytes
        """

        improper_byte_length = token_bytes(31)
        with self.assertRaises(ValueError) as error:
            _sample_ntt(improper_byte_length)

        self.assertEqual("Received an improper length, the seed must be exactly 32 bytes.", str(error.exception))
    
    def test_output_length(self):
        """
        Should fail if the output is not of length 256 (an array of 256 values)
        """

        proper_byte_length = token_bytes(32)
        output_length = 256

        test_output_length = len(_sample_ntt(proper_byte_length))

        self.assertEqual(output_length, test_output_length, "The output length should be 256")