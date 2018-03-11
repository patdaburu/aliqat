#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/10/18

from parameterized import parameterized
import unittest
from aliqat.fixed.graphs import CharClass


class TestSuite(unittest.TestCase):

    @parameterized.expand([
        (CharClass.EMPTY, '∅'),
        (CharClass.DIGIT, 'ℝ'),
        (CharClass.ALPHA, 'α'),
        (CharClass.SPECIAL, '¿'),
        (CharClass.ANY, 'ω'),
        (CharClass.ALPHA | CharClass.EMPTY, '∀'),
        (CharClass.ALPHA | CharClass.DIGIT, 'π'),
        (CharClass.ALPHA | CharClass.SPECIAL, 'غ'),
        (CharClass.DIGIT | CharClass.EMPTY, '𝕌'),
        (CharClass.DIGIT | CharClass.SPECIAL, '⊕'),
        (CharClass.SPECIAL | CharClass.EMPTY, '٭'),
        (CharClass.ANY ^ CharClass.EMPTY, '●'),
        (CharClass.ANY ^ CharClass.ALPHA, '◒'),
        (CharClass.ANY ^ CharClass.DIGIT, '◔'),
        (CharClass.ANY ^ CharClass.SPECIAL, '◎'),
    ])
    def test_fromInt_compare_correct(self, cc, s):
        """
        Arrange: Get the character representation for the enumerated value.
        Act: Compare the character representation to the second parameter (s)
        using the :py:func:`CharClass.from_int` static method.
        Assert: The character representation matches the second parameter (s).

        :param cc: the enumerated value
        :param s: the expected character representation
        """
        self.assertEqual(s, CharClass.from_int(cc))


if __name__ == '__main__':
    unittest.main()

