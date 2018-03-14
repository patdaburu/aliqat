#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/14/18
"""
.. currentmodule:: dsl
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Domain-specific language elements for fixed-width ALI parsing.

You can import this module to acquire names that are shortcuts to common
parts of the API.
"""

from .distances import *
from .graphs import CharClass


EMPTY = CharClass.EMPTY  #: an 'empty' character (whitespace, newline)
ALPHA = CharClass.ALPHA  #: an alphabet character
DIGIT = CharClass.DIGIT  #: a digit
SPECIAL = CharClass.SPECIAL  #: a known punctuation character
ANY = CharClass.ANY  #: anything
