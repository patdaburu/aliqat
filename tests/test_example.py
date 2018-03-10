#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_sample.py
.. moduleauthor:: Pat Daburu pat@daburu.net

This is a sample test module.
"""

import unittest
import aliqat


class TestSampleSuite(unittest.TestCase):
    """
    This is just an example test suite.  It will check the current project version numbers
    against the original version numbers and will start failing as soon as the current
    version numbers change.
    """
    def test_import_getVersions_originalVersions(self):
        """
        Arrange: Load the djio module.
        Act: Retrieve the versions.
        Assert: The versions match the version numbers at the time of project creation.
        """
        self.assertEqual('0.0.1', aliqat.__version__)
        self.assertEqual('0.0.1', aliqat.__release__)
