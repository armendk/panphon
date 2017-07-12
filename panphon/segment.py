# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import regex as re


class Segment(object):
    """Models a phonological segment as a vector of features."""
    def __init__(self, names, features={}, ftstr=''):
        """Construct a `Segment` object

        Args:
            names (list): ordered list of feature names
            features (dict): name-value pairs for specified features
            ftstr (unicode): a string, each /(+|0|-)\w+/ sequence of which is
            Get     interpreted as a feature specification"""
        self.n2s = {-1: '-', 0: '0', 1: '+'}
        self.s2n = {k: v for (v, k) in self.n2s.items()}
        self.names = names
        """Set a feature specification"""
        self.data = {}
        for name in names:
            if name in features:
                self.data[name] = features[name]
            else:
                self.data[name] = 0
        for m in re.finditer('(+|0|-)(\w+)', ftstr):
            v, k = m.groups()
            self.data[k] = self.s2n[v]

    def __getitem__(self, key):
        """Get a feature specification"""
        return self.data[key]

    def __setitem__(self, key, value):
        """Set a feature specification"""
        if key in self.names:
            self.data[key] = value
        else:
            raise KeyError('Unknown feature name.')

    def __repr__(self):
        """Return a string representation of a feature vector"""
        pairs = [(self.n2s[self.data[k]], k) for k in self.names]
        fts = ', '.join(['{}{}'.format(*pair) for pair in pairs])
        return '[{}]'.format(fts)

    def __iter__(self):
        """Return an iterator over the feature names"""
        return iter(self.names)

    def items(self):
        """Return a list of the features as (name, value) pairs"""
        return [(k, self.data[k]) for k in self.names]

    def iteritems(self):
        """Return an iterator over the features as (name, value) pairs"""
        return ((k, self.data[k]) for k in self.names)

    def update(self, segment):
        """Update the objects features to match `segment`.

        Args:
            segment (Segment): object containing the new feature values
        """
        self.data.update(segment)

    def match(self, other):
        """Determine whether `self`'s features are a superset of `other`'s

        Args:
            other (dict): (name, value) pairs

        Returns:
           (bool): True if superset relationship hold else False
        """
        return all([self.data[k] == v for (k, v) in features.items()])

    def __ge__(self, other):
        """Determine whether `self`'s features are a superset of `other`'s"""
        return self.match(other)

    def intersection(self, other):
        """Return dict of features shared by `self` and `other`

        Args:
            other (Segment): object with feature specifications

        Returns:
            (dict): (name, value) pairs for each shared feature
        """
        return dict(set(self.data.items()) & set(other.data.items()))

    def __and__(self, other):
        """Return dict of features shared by `self` and `other`"""
        return self.intersection(other)

    def numeric(self):
        """Return feature values as a list of integers"""
        return [self.data[k] for k in self.names]

    def string(self):
        """Return feature values as a list of strings"""
        return map(lambda x: self.n2s[x], self.numeric())

    def distance(self, other):
        """Compute a distance between `self` and `other`

        Args:
            other (Segment): object to compare with `self`

        Returns:
            (int): the sum of the absolute value of the difference between each
                   of the feature values in `self` and `other`.
        """
        return sum(abs(a - b) for (a, b) in zip(self.numeric(), other.numeric()))

    def norm_distance(self, other):
        """Compute a distance, normalized by vector length

        Args:
            other (Segment): object to compare with `self`

        Returns:
            (float): the sum of the absolute value of the difference between
                     each of the feature values in `self` and `other`, divided
                     by the number of features per vector.
        """
        return self.distance(other) / len(self.names)

    def __sub__(self, other):
        return self.norm_distance(other)

    def hamming_distance(self, other):
        return sum(int(a != b) for (a, b) in zip(self.numeric(), other.numeric()))

    def norm_hamming_distance(self, other):
        return self.hamming_distance(other) / len(self.names)
