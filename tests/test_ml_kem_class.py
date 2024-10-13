"""
ML kem class test cases.
"""

import unittest
from ml_kem.ml_kem import MLKEM


class TestMLKemTestCase(unittest.TestCase):
    """
    ML_KEM tests.
    """

    def test_pm512_key_generation(self):
        """
        Test parameter set 512 creates keys
        """
        ml_kem = MLKEM("512")

        ek, dk = ml_kem.generate_keys()

        self.assertEqual(800, len(ek))
        self.assertEqual(1632, len(dk))

    def test_pm768_key_generation(self):
        """
        Test parameter set 768 creates keys
        """
        ml_kem = MLKEM("768")

        ek, dk = ml_kem.generate_keys()

        self.assertEqual(1184, len(ek))
        self.assertEqual(2400, len(dk))

    def test_pm1024_key_generation(self):
        """
        Test parameter set 1024 creates keys
        """
        ml_kem = MLKEM("1024")

        ek, dk = ml_kem.generate_keys()

        self.assertEqual(1568, len(ek))
        self.assertEqual(3168, len(dk))
