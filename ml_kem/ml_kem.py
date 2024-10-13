"""
The main user facing ml-kem tool file.
"""

from utils.parameters import P512, P768, P1024
from utils.functions import ml_kem_gey_gen


class MLKEM:
    """
    ML_KEM
    """

    def __init__(self, parameter_set="1024") -> None:

        if parameter_set == "512":
            self.pm_set = P512
        elif parameter_set == "768":
            self.pm_set = P768
        else:
            self.pm_set = P1024

    def generate_keys(self):
        """
        Creates the keys
        """
        return ml_kem_gey_gen(self.pm_set.k)
