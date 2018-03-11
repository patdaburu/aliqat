#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/10/18

import unittest
from parameterized import parameterized
from aliqat.fixed.graphs import CharClass, Graph


class TestSuite(unittest.TestCase):
    """
    Tests of the :py:class:`Graph` class.
    """
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

    @parameterized.expand([
        ('a', 'a', 'a', 'a'),
        ('b', 'b', 'b', 'b'),
        ('a', 'b', 'c', CharClass.ALPHA.char),
        ('a', '1', 'b', CharClass.from_int(CharClass.ALPHA | CharClass.DIGIT)),
        ('a', '1', '2', CharClass.from_int(CharClass.ALPHA | CharClass.DIGIT)),
        ('a', ' ', ' ', CharClass.from_int(CharClass.ALPHA | CharClass.EMPTY)),
        ('a', '1', ' ', CharClass.from_int(CharClass.ANY ^ CharClass.SPECIAL)),
        ('a', '1', None, CharClass.from_int(CharClass.ANY ^ CharClass.SPECIAL)),
        ('a', '!', ' ', CharClass.from_int(CharClass.ANY ^ CharClass.DIGIT)),
        ('a', '!', None, CharClass.from_int(CharClass.ANY ^ CharClass.DIGIT)),
        ('a', None, ' ', CharClass.from_int(CharClass.ALPHA | CharClass.EMPTY)),
        ('a', '!', '?',
         CharClass.from_int(CharClass.ALPHA | CharClass.SPECIAL)),
        ('1', '1', '1', '1'),
        ('1', '2', '3', CharClass.DIGIT.char),
        ('1', ' ', '2', CharClass.from_int(CharClass.DIGIT | CharClass.EMPTY)),
        ('1', None, '2', CharClass.from_int(CharClass.DIGIT | CharClass.EMPTY)),
        ('1', '!', '3',
         CharClass.from_int(CharClass.DIGIT | CharClass.SPECIAL)),
        ('!', '!', '!', '!'),
        ('!', '+', '?', CharClass.SPECIAL.char),
        ('!', ' ', '+',
         CharClass.from_int(CharClass.SPECIAL | CharClass.EMPTY)),
        ('!', None, '+',
         CharClass.from_int(CharClass.SPECIAL | CharClass.EMPTY)),
        ('a', ' ', '!', CharClass.from_int(CharClass.ANY ^ CharClass.DIGIT)),
        ('a', None, '!', CharClass.from_int(CharClass.ANY ^ CharClass.DIGIT)),
        ('a', '1', '!', CharClass.from_int(CharClass.ANY ^ CharClass.EMPTY)),
        (' ', '1', '!', CharClass.from_int(CharClass.ANY ^ CharClass.ALPHA)),
        (None, '1', '!', CharClass.from_int(CharClass.ANY ^ CharClass.ALPHA)),
    ])
    def test_graph_conflateTwice_correct(self, a, b, c, s):
        """
        Arrange: Create graphs from first three parameters (a, b, and c).
        Act: Conflate the graphs.
        Assert: The conflated graph matches the last parameter.

        :param a: the first graph input
        :param b: the second graph input
        :param c: the third parameter
        :param s: the expected result of conflation
        """
        for _a, _b, _c in [
            (a, b, c), (c, a, b), (b, a, c)
        ]:  # Rotate for each test run.
            g1 = Graph(_a)
            g2 = Graph(_b)
            g3 = Graph(_c)
            g1.conflate(g2)
            g1.conflate(g3)
            self.assertEqual(
                s, str(g1),
                "a={}; b={}; c={}".format(repr(_a), repr(_b), repr(_c)))

    @parameterized.expand([
        ('a', 'a', 'a', 'a', 'a'),
        ('a', '1', '!', ' ', CharClass.ANY.char),
        ('a', '1', '!', None, CharClass.ANY.char)
    ])
    def test_graph_conflateThrice_correct(self, a, b, c, d, s):
        """
        Arrange: Create graphs from first two parameters (a, b, c, and d).
        Act: Conflate the graphs.
        Assert: The conflated graph matches the last parameter.

        :param a: the first graph input
        :param b: the second graph input
        :param c: the third parameter
        :param d: the fourth parameter
        :param s: the expected result of conflation
        """
        for _a, _b, _c, _d in [
            (a, b, c, d), (d, a, b, c), (c, d, a, b), (b, c, d, a)
        ]:  # Rotate for each test run.
            g1 = Graph(_a)
            g2 = Graph(_b)
            g3 = Graph(_c)
            g4 = Graph(_d)
            g1.conflate(g2)
            g1.conflate(g3)
            g1.conflate(g4)
            self.assertEqual(
                s, str(g1),
                "a={}; b={}; c={}; d={}".format(
                    repr(_a), repr(_b), repr(_c), repr(_d)))


if __name__ == '__main__':
    unittest.main()

