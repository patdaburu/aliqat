#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/10/18

import unittest
from parameterized import parameterized
from aliqat.graphs import CharClass, Graph


class TestSuite(unittest.TestCase):

    @parameterized.expand([
        ('a', 'a', 'a'),
        ('b', 'b', 'b'),
        ('a', 'b', CharClass.ALPHA.char),
        ('a', '1', CharClass.from_int(CharClass.ALPHA | CharClass.DIGIT)),
        ('a', ' ', CharClass.from_int(CharClass.ALPHA | CharClass.EMPTY)),
        ('a', None, CharClass.from_int(CharClass.ALPHA | CharClass.EMPTY)),
        ('a', '!', CharClass.from_int(CharClass.ALPHA | CharClass.SPECIAL)),
        ('1', '1', '1'),
        ('1', '2', CharClass.DIGIT.char),
        ('1', ' ', CharClass.from_int(CharClass.DIGIT | CharClass.EMPTY)),
        ('1', None, CharClass.from_int(CharClass.DIGIT | CharClass.EMPTY)),
        ('1', '!', CharClass.from_int(CharClass.DIGIT | CharClass.SPECIAL)),
        ('!', '!', '!'),
        ('!', '+', CharClass.SPECIAL.char),
        ('!', ' ', CharClass.from_int(CharClass.SPECIAL | CharClass.EMPTY)),
        ('!', None, CharClass.from_int(CharClass.SPECIAL | CharClass.EMPTY))
    ])
    def test_graph_conflateOnce_correct(self, a, b, s):
        """
        Arrange: Create graphs from first two parameters (a and b).
        Act: Conflate the graphs.
        Assert: The conflated graph matches the third parameter.

        :param a: the first graph input
        :param b: the second graph input
        :param s: the expected result of conflation
        """
        for _a, _b in [(a, b), (b, a)]:  # Invert a an b for each test run.
            g1 = Graph(_a)
            g2 = Graph(_b)
            g1.conflate(g2)
            self.assertEqual(
                s, str(g1), "a={}; b={}".format(repr(_a), repr(_b)))

# class ParamaterizedSampleTestSuite(unittest.TestCase):
#     """
#     This is just an example test suite that demonstrates the very useful
#     `parameterized` module.  It contains a test in which the squares of the
#     first two parameters are added together and passes if that sum equals the
#     third parameter.
#     """
#     @parameterized.expand([
#         (1, 2, 5),
#         (3, 4, 25)
#     ])
#     def test_ab_addSquares_equalsC(self, a, b, c):
#         """
#         Arrange: Acquire the first two parameters (a and b).
#         Act: Add the squares of the first two parameters (a and b).
#         Assert: The sum of the squares equals the third parameter (c).
#
#         :param a: the first parameter
#         :param b: the second parameter
#         :param c: the result of adding the squares of a and b
#         """
#         self.assertEqual(c, a*a + b*b)



if __name__ == '__main__':
    unittest.main()

