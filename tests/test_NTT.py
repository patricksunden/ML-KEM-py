"""
Test file.
"""

# 

import unittest
from secrets import token_bytes
from utils.functions import _sample_ntt, ntt, inverse_ntt, multiply_ntt, base_case_multiply

class Test_ntt_functions(unittest.TestCase):

######################
## sample_NTT tests ##
######################

    def sample_ntt_improper_length(self):
        """
        Should raise ValueError if the length of the input is less than 32 bytes
        """

        improper_byte_length = token_bytes(31)
        with self.assertRaises(ValueError) as error:
            _sample_ntt(improper_byte_length)

        self.assertEqual("Received an improper length, the seed must be exactly 32 bytes.", str(error.exception))
    
    def sample_ntt_output_length(self):
        """
        Should fail if the output is not of length 256 (an array of 256 values)
        """

        proper_byte_length = token_bytes(32)
        output_length = 256

        output_length1 = len(_sample_ntt(proper_byte_length))

        self.assertEqual(output_length, output_length1, "The output length should be 256")



#####################
##    NTT tests    ##
#####################

    def ntt_output_length(self):
        """
        Should fail if the output is not of length 256 (an array of 256 values)
        """

        input_array = [0] * 256
        output_length = 256

        output_length1 = len(ntt(input_array))

        self.assertEqual(output_length, output_length1, "The output length should be 256")

    def test_ntt_false_input_type(self):

        f = (1,) * 256

        with self.assertRaises(TypeError) as error:
            ntt(f)
        
        self.assertEqual(
            "The input needs to be a list.", str(error.exception))



#######################
## inverse ntt tests ##
#######################

    def test_ntt_inverse_output_length(self):
        """
        Should fail if the output is not of length 256 (an array of 256 values)
        """

        f = [1] * 256
        output_length = 256

        output_length1 = len(inverse_ntt(f))

        self.assertEqual(output_length, output_length1, "Received an improper length, the array length must be exactly 256.")

    def test_ntt_false_input_type(self):

        f = (1,) * 256

        with self.assertRaises(TypeError) as error:
            inverse_ntt(f)
        
        self.assertEqual(
            "The input needs to be a list.", str(error.exception))



#########################
## MULTIPLY_NTT tests  ##
#########################

    def test_multiply_ntt_output_length(self):

        f = [1] * 256
        g = [2] * 256

        expected_length = 256
        h = multiply_ntt(f, g)
        self.assertEqual(len(h), expected_length)

    def test_multiply_ntt_zero(self):

        expected_output = [0] * 256
        f = [0] * 256
        g = [2] * 256

        h = multiply_ntt(f, g)
        self.assertEqual(h, expected_output)

    def test_multiply_ntt_input(self):

        f = [0] * 255
        g = [2] * 256

        with self.assertRaises(ValueError) as error:
            multiply_ntt(f, g)
        
        self.assertEqual(
            "The length of the input arrays need to be exactly 256.", str(error.exception))
        
    def test_multiply_ntt_input(self):

        f = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        g = [2] * 256

        with self.assertRaises(TypeError) as error:
            multiply_ntt(f, g)
        
        self.assertEqual(
            "The input needs to be a list.", str(error.exception))



###############################
## BASE_CASE_MULTIPLY tests  ##
###############################

    def test_base_case_multiply(self):

        # Test basic stuff with known outputs
        self.assertEqual(base_case_multiply(1, 2, 3, 4, 5), (43, 10))
        self.assertEqual(base_case_multiply(0, 0, 0, 0, 0), (0, 0))

    def test_base_case_int_input(self):

        a0 = "k"
        a1 = 1
        b0 = 2
        b1 = 3
        gamma = 4

        with self.assertRaises(TypeError) as error:
            base_case_multiply(a0, a1, b0, b1, gamma)

        self.assertEqual(
        "The inputs need to be of type int", str(error.exception))