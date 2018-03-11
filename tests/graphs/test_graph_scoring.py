#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/11/18

from aliqat.fixed.graphs import Graph, CharClass
from aliqat.fixed.distances import *
from parameterized import parameterized
import unittest


class TestSuite(unittest.TestCase):

    @parameterized.expand([
        ('a', 'a', 0),
        ('a', 'b', LITERAL_MISMATCH),
        ('aa', 'ab', LITERAL_MISMATCH),
        ('aa', 'bb', LITERAL_MISMATCH * 2),
        (' ', ' ', 0),
        (' ', 'a', LITERAL_MISMATCH),
        ('  ', ' a', LITERAL_MISMATCH),
        ('  ', 'aa', LITERAL_MISMATCH * 2),
        ('  ', '', LITERAL_MISMATCH * 2),
        ('', '  ', LENGTH_MISMATCH_MULTIPLIER * 2),
        ('1', '1', 0),
        ('1', 'a', LITERAL_MISMATCH),
        ('1', 'a ', LITERAL_MISMATCH + LENGTH_MISMATCH_MULTIPLIER),
        ('*', '*', 0),
        ([CharClass.ANY], 'a', 4)
    ])
    def test_graph_compare_score(self, g1, g2, score):
        _g1 = Graph(g1)
        _g2 = Graph(g2)
        self.assertEqual(
            score,
            _g1.distance(_g2),
            "g1={}; g2={}".format(repr(g1), repr(g2))
        )


if __name__ == '__main__':
    unittest.main()

