#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/11/18

from aliqat.fixed.graphs import Graph, CharClass
from aliqat.fixed.distances import *
from parameterized import parameterized
import unittest


class TestSuite(unittest.TestCase):

    @parameterized.expand([
        # ('a', 'a', 0),
        # ('a', 'b', LITERAL_MISMATCH),
        # ('aa', 'ab', LITERAL_MISMATCH),
        # ('aa', 'bb', LITERAL_MISMATCH * 2),
        # (' ', ' ', 0),
        # (' ', 'a', LITERAL_MISMATCH),
        # ('  ', ' a', LITERAL_MISMATCH),
        # ('  ', 'aa', LITERAL_MISMATCH * 2),
        # ('  ', '', LITERAL_MISMATCH * 2),
        # ('', '  ', LENGTH_MISMATCH_MULTIPLIER * 2),
        # ('1', '1', 0),
        # ('1', 'a', LITERAL_MISMATCH),
        # ('1', 'a ', LITERAL_MISMATCH + LENGTH_MISMATCH_MULTIPLIER),
        # ('*', '*', 0),
        # ('*', '1', LITERAL_MISMATCH),

        # ([CharClass.ALPHA], 'a', 1),
        # ([CharClass.ALPHA | CharClass.DIGIT], 'a', 2),
        # ([CharClass.ALPHA | CharClass.DIGIT | CharClass.SPECIAL], 'a', 3),
        ([CharClass.EMPTY | CharClass.DIGIT | CharClass.SPECIAL], 'a', 7),
        ([CharClass.ANY ^ CharClass.ALPHA], 'a', 7),  # (Same as above.)
        ([CharClass.ANY], 'a', 7)

        # ([CharClass.ANY], 'a', 3),
        # ([CharClass.ANY], 'a', 3),
        # ([CharClass.ANY], 'a', 3),
        # ([CharClass.ALPHA], 'b',
        #  FUZZY_MATCH_PENALTY + 1 + FUZZY_MATCH_MULTIPLIER)
    ])
    def test_graph_distance_score(self, g1, g2, distance):
        """
        Arrange: Create two graphs.
        Act: Evaluate the distance between the second and the first.
        Assert: The expected distance is observed.

        :param g1: the contents of the first graph
        :param g2: the contents of the second graph
        :param distance: the expected distance between the graphs
        """
        _g1 = Graph(g1)
        _g2 = Graph(g2)
        self.assertEqual(
            distance,
            _g1.distance(_g2),
            "g1={}; g2={}".format(repr(g1), repr(g2))
        )


if __name__ == '__main__':
    unittest.main()

