#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/11/18
"""
.. currentmodule:: scores
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Fixed scoring values.
"""

LITERAL_MISMATCH = 5  #: mismatch of a literal characters
FUZZY_MATCH = 1  #: a non-literal ('fuzzy') string match
LENGTH_MISMATCH = 2  #: a length mismatch between graphs
FUZZY_SWING_MISS = 0.25  #:  a single bit miss in a fuzzy match
FUZZY_STRIKEOUT = FUZZY_MATCH * 3
