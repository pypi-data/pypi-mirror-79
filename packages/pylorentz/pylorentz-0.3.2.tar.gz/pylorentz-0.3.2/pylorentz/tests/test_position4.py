"""
Unittests for the class Momentum4
"""

import unittest
import numpy as np
import cmath
from pylorentz import Position4


class Position4TestCase(unittest.TestCase):
    """
    Test the implementation of Position4.
    """
    def assertListAlmostEqual(self, list_a, list_b, *args, **kwds):
        list_a = list(list_a)
        list_b = list(list_b)
        if len(list_a) != len(list_b):
            self.assertEqual(list_a, list_b)

        for a, b in zip(list_a, list_b):
            self.assertAlmostEqual(a, b, *args, **kwds)

    def test_init(self):
        """
        Check that a instantiation with all four componentes returns the
        correct vector.
        """
        position = Position4(100, 2.5, 1.23, 1.777)
        self.assertAlmostEqual(position.t, 100)
        self.assertAlmostEqual(position.x, 2.5)
        self.assertAlmostEqual(position.y, 1.23)
        self.assertAlmostEqual(position.z, 1.777)

    def test_single_item(self):
        """Check single-item arrays don't turn into scalars."""
        position = Position4([1], [0], [1], [1])

        self.assertListAlmostEqual(position.t, [1])
        self.assertListAlmostEqual(position.x, [0])
        self.assertListAlmostEqual(position.y, [1])
        self.assertListAlmostEqual(position.z, [1])
