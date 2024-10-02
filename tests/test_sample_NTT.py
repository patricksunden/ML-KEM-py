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

        improper_byte_length = token_bytes(10)

        with self.assertRaises(ValueError) as error:
            _sample_ntt(improper_byte_length)

        self.assertEqual(
            "Received an improper length", str(error.exception))
        
Test_Sample_ntt.test_improper_length()
    
