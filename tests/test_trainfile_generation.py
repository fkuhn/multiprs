# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from multiprs import corpustools
from lxml import etree
import re
import pytest
import os

tdata = os.path.abspath("/tests/tdata/")

def test_traindata():
    """
    this test runs to find non-parsed element-tiers in the exmaralda sources
    :return:
    """
    traindata_iterator = corpustools.make_tier_tuple_list(tdata)
    for fname, token, pos in traindata_iterator:
        assert fname != None
        assert token != None
        assert pos != None

def test_v_tupels():
    """
    Are all verbal tier tupels created without None values?
    :return:
    """
    traindata_iterator = corpustools.make_tier_tuple_list(tdata)
    tlist = [(fname, v_tupels, pos_tupels) for fname, v_tupels, pos_tupels in traindata_iterator]

    for fname, v_tupels, pos_tupels in tlist:

        assert len(v_tupels) > 1
        for tupel in v_tupels:
            timestamp = tupel[0]
            value = tupel[1]
            assert timestamp != None
            assert value != None


def test_pos_tupels():
    """
    Are all pos tier tupels created without None values?
    :return:
    """
    traindata_iterator = corpustools.make_tier_tuple_list(tdata)
    for fname, v_tupels, pos_tupels in traindata_iterator:

        assert len(pos_tupels) > 1
        for tupel in pos_tupels:
            timestamp = tupel[0]
            value = tupel[1]
            assert timestamp != None
            assert value != None


def test_tokenpos():
    trdata = corpustools.make_tier_tuple_list(tdata)
    trfiles = {}

    # check if trdata is iterable
    assert hasattr(trdata, '__iter__')
    counter = 0
    for fn, t, p in trdata:
        counter += 1
        tp = []

        for token in t:
            for pos in p:
                if token[0] == pos[0]:
                    tp.append((token[0], token[1], pos[1]))
        trfiles.update({fn: tp})

    assert len(trfiles) == counter