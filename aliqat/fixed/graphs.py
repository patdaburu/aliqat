#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by pat on 3/8/18
"""
.. currentmodule:: graphs
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Say something descriptive about the 'grids' module.
"""

from enum import IntFlag
from functools import reduce
import os
from aliqat.fixed.distances import *
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

    _BIN_FIXER = CharClass.ANY + 1

    def __init__(self, s: str):  # TODO: Optional parameter to set minimum size.
        # If the caller actually passed us a list...
        if isinstance(s, list):
            # ...we'll just copy it.
            self._graph = s[:]
        else:
            self._graph = list(s) if s is not None else []

    def __iter__(self):
        return iter(self._graph)

    def conflate(self, other: 'Graph'):
        other_graph = [item for item in other]
        if len(other_graph) > len(self._graph):
            self._graph.extend([' '] * (len(other_graph) - len(self._graph)))
        elif len(self._graph) > len(other_graph):  # If this graph is longer...
            # ...extend the other graph with whitespace.
            other_graph.extend([' '] * (len(self._graph) - len(other_graph)))
        for i in range(0, len(other_graph)):
            c = other_graph[i]
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
                # If we find a length-mismatch at this position, that carries
                # a distance of its own.
                scores[i] = LENGTH_MISMATCH
            else:
                # Otherwise, we'll encode both values. (We OR the higher-order
                # bit to make sure the representations of the binary numbers
                # are always the same width.  This means we end up with an
                # extra 'on' bit on the left.  Notice that we have to subtract 1
                # when we're counting bits in a few spots below to account for
                # that.)
                slf_enc = self._BIN_FIXER | self._encode(self_graph[i])
                oth_enc = self._BIN_FIXER | self._encode(oth)
                # AND the encodings together.
                result_fixed = slf_enc & oth_enc
                # A 'strikeout' is the case in which *none* of the bits matched.
                strikeout = (bin(result_fixed).count('1') - 1 == 0)
                # If none of the bits matched...
                if strikeout:
                    # ...that's the maximum distance.
                    dist = FUZZY_STRIKEOUT
                else:
                    # Let's figure out how many 'swings' we took (i.e. how many
                    # 'on' bits there are in this graph's encoding).
                    swings = bin(slf_enc).count('1') - 1
                    # Now, how many of those 'swings' connected (ie. how many
                    # 'on' bits in this graph's encoding matched 'on' bits in
                    # the other graph's encoding)?
                    hits = bin(result_fixed).count('1') - 1
                    # The distance is now calculated as a function of the
                    # number of swings (which add distance) to the number of
                    # hits (which subtract distance).
                    dist = FUZZY_MATCH + ((swings - hits) * FUZZY_SWING_MISS)
                # We can now add this distance to the collection.
                scores[i] = dist
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
        classification = distances[0][0]
        graph = self._conflated[classification]
        return classification, graph

