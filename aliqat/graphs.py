#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/8/18
"""
.. currentmodule:: grids
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the 'grids' module.
"""

from enum import IntFlag
from functools import reduce
import os
from .distances import *
from typing import Dict, List, Tuple


class CharClass(IntFlag):
    """
    This is an enumeration of significant character types expressed as flags
    that may be combined to express the intersection of classes.
    """
    EMPTY = 1  #: an 'empty' character (whitespace, newline)
    ALPHA = 2  #: an alphabet character
    DIGIT = 4  #: a digit
    SPECIAL = 8  #: a known punctuation character
    ANY = 15  #: anything

    @property
    def char(self) -> str:
        """
        Get the single-character string representation for this enumerated
        value.

        :return: the single-character string representation
        """
        try:
            return CharClass.from_int(self)
        except KeyError:
            raise RuntimeError('No character is defined.')

    @staticmethod
    def from_int(i: int):
        """
        Get the single-character string representation for an enumerated
        value.

        :param i: the integer value
        :return: the single-character string representation
        :raises KeyError: if no single-character string representation is
        defined
        """
        return {
            CharClass.EMPTY: '∅',
            CharClass.ALPHA: 'α',
            CharClass.DIGIT: 'ℝ',
            CharClass.SPECIAL: '¿',
            CharClass.ANY: 'ω',
            CharClass.ALPHA | CharClass.DIGIT: 'π',
            CharClass.ALPHA | CharClass.EMPTY: '∀',
            CharClass.ALPHA | CharClass.SPECIAL: 'غ',
            CharClass.DIGIT | CharClass.EMPTY: '𝕌',
            CharClass.DIGIT | CharClass.SPECIAL: '⊕',
            CharClass.SPECIAL | CharClass.EMPTY: '٭',
            CharClass.ANY ^ CharClass.EMPTY: '●',
            CharClass.ANY ^ CharClass.ALPHA: '◒',
            CharClass.ANY ^ CharClass.DIGIT: '◔',
            CharClass.ANY ^ CharClass.SPECIAL: '◎'
        }[i]


class _LengthMismatch(object):
    """
    This is a flag type used to indicate a character in one graph that has no
    corresponding character in another graph to which it's being compared.
    """
    def __init__(self):
        raise RuntimeError('Do not instantiate this class.')


class Graph(object):

    def __init__(self, s: str, classification: str=None):  # TODO: Optional parameter to set minimum size.
        self._graph = list(s) if s is not None else [' ']

    def __iter__(self):
        return iter(self._graph)

    def conflate(self, other: 'Graph'):
        i = 0
        for c in other:
            # Conflate the current value at the specified index in this graph
            # with the value from the other graph.
            try:
                self._graph[i] = self._conflate(self._graph[i], c)
            except IndexError:
                self._graph.extend(self._conflate(self._graph[i], c))
            i += 1

    def distance(self, other: 'Graph') -> float:
        # Extract the items in the other graph.
        other_graph = [item for item in other]
        len_other = len(other_graph)
        # Copy this graph.
        self_graph: List = self._graph[:]
        len_self = len(self_graph)
        # Make sure the graph lists are of equal length.
        if len_other > len_self:
            self_graph.extend([_LengthMismatch] * (len_other - len_self))
        elif len_self > len_other:
            other_graph.extend([_LengthMismatch] * (len_self - len_other))
        # Create an array to hold the scores.  (We can initialize it to the
        # length of the other graph because they should now both be the same.)
        scores = [0] * len(other_graph)
        # Let's compare each character.
        for i in range(0, len(other_graph)):
            slf = self_graph[i]
            oth = other_graph[i]
            # If the value in this graph is a string...
            if isinstance(slf, str):
                # If the values match entirely...
                if slf == oth:
                    # ...there is no distance.
                    continue
                else:
                    # Otherwise we count the distance of a literal mismatch.
                    scores[i] = LITERAL_MISMATCH
            elif slf == _LengthMismatch or oth == _LengthMismatch:
                scores[i] = LENGTH_MISMATCH_MULTIPLIER
            else:
                # Otherwise, we'll encode both values.
                slf_enc = self._encode(self_graph[i])
                oth_enc = self._encode(oth)
                # The comparison will be a bitwise AND.
                cmp = slf_enc & oth_enc
                scores[i] = (bin(cmp).count('1')) * FUZZY_MATCH_MULTIPLIER
        # Sum the scores...
        _sum = reduce((lambda x, y: x + y), scores)
        # ...and return 'em.
        return _sum

    @staticmethod
    def _conflate(a: str or CharClass, b: str or CharClass):
        # If the values are equal, return either one.
        if a == b:
            return a
        t = (a, b)  # Collect the values.
        # If one of them is None, return the other one.
        if None in t:
            return [c for c in t if c is not None][0]
        # Make sure we're dealing with single characters from here on in.
        if isinstance(a, str) and len(a) != 1:
            raise ValueError('a must be a single character, flag, or None.')
        if isinstance(b, str) and len(b) != 1:
            raise ValueError('b must be a single character, flag, or None.')
        # Encode each value.
        a_enc = Graph._encode(a)
        b_enc = Graph._encode(b)
        # The conflation result is a's encoding OR (binary) b's encoding.
        return a_enc | b_enc

    @staticmethod
    def _encode(c: str) -> CharClass:
        # TODO: Cache results!!!!
        # TODO: Move special lists of characters to a more visible location!!!
        # If the argument is already character class (or just an int)...
        if isinstance(c, int):
            return c  # ...we already have our answer.
        if c is not None and len(c) != 1:  # Sanity check!  # TODO: Use common logic for check.
            raise ValueError('c must be a single character or None.')
        # Classify the input.
        if c is None or c in [' ', '\r', '\n']:  # TODO: Move character lists!
            return CharClass.EMPTY
        elif c.isdigit():
            return CharClass.DIGIT
        elif c.isalpha():
            return CharClass.ALPHA
        elif c in ['+', '-', ',', ':', '*', '!', '?', '<', '>', '.']:  # TODO: Move character lists!
            return CharClass.SPECIAL
        else:
            return CharClass.ANY

    @staticmethod
    def _str(i: str or CharClass):
        try:
            return CharClass.from_int(i)
        except KeyError:
            return i

    def __str__(self):
        return ''.join([self._str(i) for i in self._graph])

    @staticmethod
    def from_file(path: os.PathLike) -> 'Graph':
        """
        Load a :py:class:`Graph` from a file.

        :param path: the file path
        :return: the loaded graph
        """
        with open(path) as f:
            s = f.read()
            return Graph(s)


class Classifier(object):

    def __init__(self):
        self._graphs: Dict[str, List[Graph]] = {}
        self._conflated: Dict[str, Graph] = {}

    def train(self, classification: str, graph: Graph):
        # Collect the graphs.
        try:
            self._graphs[classification].append(graph)
        except KeyError:
            self._graphs[classification] = [graph]
        # Conflate this graph with the others.
        try:
            self._conflated[classification].conflate(graph)
        except KeyError:
            self._conflated[classification] = graph

    def classify(self, graph: Graph):
        # TODO: Asyn processing would prolly be a good idea.
        # TODO: Create a NamedTuple to make the code a little easier to read.
        distances: List[Tuple] = []
        for clsf, conflated in self._conflated.items():
            distances.append((clsf, conflated.distance(graph)))  # TODO: Named tuple!
        # Sort the distances list according to the distance (the second item in
        # the tuple).
        distances.sort(key=lambda t: t[1])
        # Return the first classification.
        return distances[0][0]

