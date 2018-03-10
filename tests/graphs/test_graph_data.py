#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/10/18

from aliqat.graphs import Graph
import unittest
from os import listdir
from os.path import abspath, dirname, join
from typing import Dict


class TestSuite(unittest.TestCase):


    def test_arrange_act_assert(self):
        print()
        train_dir = join(abspath(dirname(__file__)), 'data', 'train')
        test_dir = join(abspath(dirname(__file__)), 'data', 'test')
        print(train_dir)
        print(test_dir)

        # Load the training graphs.
        graphs: Dict[str, Graph] = {}

        for d in sorted(listdir(train_dir)):
            dpath = join(train_dir, d)
            for f in listdir(dpath):
                fpath = join(dpath, f)
                graph = Graph.from_file(fpath)
                if d in graphs:
                    graphs[d].conflate(graph)
                else:
                    graphs[d] = graph

        for k,g in graphs.items():
            print('{}\n{}\n{}\n'.format(k, '=' * 20, str(g)))




        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

