from typing import Callable
import unittest

from . import fonc


class TestFonc(unittest.TestCase):
    def test_makes_callable(self):
        self.assertTrue(isinstance(fonc(""""""), Callable))

    # def test_lambda_eval(self):
    #     self.assertTrue(fonc("lambda x: x")(2), 2)

    def test_def_eval(self):
        self.assertTrue(
            fonc(
                """
def identity(x):
    return x
        """
            )(2),
            2,
        )
