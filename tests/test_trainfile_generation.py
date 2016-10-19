# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from multiprs import corpustools
from lxml import etree
import re
import pytest
import ose
# Path to directory with manually pos tagged exb files
germanExmaraldaTrain = "/home/kuhn/ownCloud/2multilit/Data/Training/Traingsdaten DE/"
englishExmaraldaTrain = "/home/kuhn/ownCloud/2multilit/Data/Training/Trainingsdaten EN/"
turkishExmaraldaTrain = "/home/kuhn/ownCloud/2multilit/Data/Training/Trainingsdaten_TR/Block1-5"
# Path to directory to exb files without pos tags 

# Path to directory to write finalized training files to
german_tt_trainfile = "tt_trainingfile_DE.txt"
english_tt_trainfile = "tt_trainingfile_EN.txt"
turkish_brill_trainfile = "tt_trainingfile_TR.txt"

# def tokenpos(trdata):
#     trfiles = {}
#     try:
#         for fn, t, p in trdata:
#             tp = []
#             for token in t:
#                 tkn = token[1].rstrip(' \t\n')
#                 for pos in p:
#                     if pos[1] == None:
#                         continue
#                     if token[0] == pos[0]:
#                         tp.append((token[0], tkn, pos[1].rstrip(' \t\n')))
#                         continue
#                 if tkn == u'.':
#                     tp.append((token[0], tkn, '.$'))
#                     continue
#                 elif tkn == u',':
#                     tp.append((token[0], tkn, ',$'))
#                     continue
#                 elif tkn == u';':
#                     tp.append((token[0], tkn, ';$'))
#                     continue
#                 elif tkn == u'?':
#                     tp.append((token[0], tkn, '?$'))
#                     continue
#                 elif tkn == u'!':
#                     tp.append((token[0], tkn, '!$'))
#                     continue
#                 elif tkn == u'• • •' or tkn == '• •' or tkn == '•':
#                     tp.append((token[0], tkn, 'PAUSE'))
#                     continue
#                 elif re.match('\(\(\d,\ds\)\)',tkn):
#                     tp.append((token[0], tkn, 'PAUSE'))
#                     continue
#
#             trfiles.update({fn: tp})
#     except TypeError:
#         print("tokenpos: none type reference")
#     return trfiles

#
# def tokenpos(trdata):
#     trfiles = {}
#     for fn, t, p in trdata:
#         tp = []
#
#         for token in t:
#             for pos in p:
#                 if token[0] == pos[0]:
#                     tp.append((token[0], token[1], pos[1]))
#         trfiles.update({fn: tp})
#
#     return trfiles
#
#
# def create_tagger_trainingfile(trainingsources, trainingfilepath, type='treetagger'):
#     """
#     creates a textfile conform to the train-tree-tagger input format
#     (verticalized token \t pos \n lines of a file)
#     param: traingsources: filepath to all .exb training files
#     param: trainingfilepath: path and filename of the text trainingfile
#     param: type: either treetagger or brill to determine the style of the trainingfile.
#     """
#     traindata_iterator = corpustools.ExmaTokenPOSIterator(trainingsources)
#     data = tokenpos(traindata_iterator)
#
#     with open(trainingfilepath,  "w") as tt_trainingfile:
#         for postuples_tier in data.itervalues():
#         # print("{}{}".format(postuple_tier, "\n"*2))
#             for postuple in postuples_tier:
#                 if type=='treetagger':
#                     line = "{}\t{}\t{}".format(postuple[1], postuple[2], u'\n')
#                 elif type=='brill':
#                     line = "{}|{}{}".format(postuple[1], postuple[2], u'\n')
#                 line8 = line.encode('UTF-8')
#                 try:
#                     tt_trainingfile.write(line8)
#                 except UnicodeEncodeError:
#                     print("unicode error in tuple {}".format(postuple))

=======

tdata = os.path.abspath("./tdata/")
>>>>>>> 3480e95... reformatted test training file

def test_german_traindata():
    """
    this test runs to find non-parsed element-tiers in the exmaralda sources
    :return:
    """
    traindata_iterator = corpustools.ExmaTokenPOSIterator(germanExmaraldaTrain)
    for fname, token, pos in traindata_iterator:
        assert fname != None
        assert token != None
        assert pos != None

=======
tdata = os.path.abspath("tdata/")
>>>>>>> 433e440... corrected tesdata path refernce

<<<<<<< HEAD
def test_english_traindata():
    """
    this test runs to find non-parsed element-tiers in the exmaralda sources
    :return:
    """
    traindata_iterator = corpustools.ExmaTokenPOSIterator(englishExmaraldaTrain)
    assert hasattr(traindata_iterator, '__iter__')
    for fname, token, pos in traindata_iterator:
        assert fname != None
        assert token != None
        assert pos != None


def test_german_v_tupels():
=======
def test_v_tupels():
>>>>>>> 3480e95... reformatted test training file
    """
    Are all verbal tier tupels created without None values?
    :return:
    """
    traindata_iterator = corpustools.ExmaTokenPOSIterator(germanExmaraldaTrain)
    for fname, v_tupels, pos_tupels in traindata_iterator:

        assert len(v_tupels) > 1
        for tupel in v_tupels:
            timestamp = tupel[0]
            value = tupel[1]
            assert timestamp != None
            assert value != None


def test_english_v_tupels():
    """
    Are all verbal tier tupels created without None values?
    :return:
    """
    traindata_iterator = corpustools.ExmaTokenPOSIterator(englishExmaraldaTrain)
    for fname, v_tupels, pos_tupels in traindata_iterator:

        assert len(v_tupels) > 1
        for tupel in v_tupels:
            timestamp = tupel[0]
            value = tupel[1]
            assert timestamp != None
            assert value != None


<<<<<<< HEAD
def test_german_pos_tupels():
    """
    Are all pos tier tupels created without None values?
    :return:
    """
    traindata_iterator = corpustools.ExmaTokenPOSIterator(germanExmaraldaTrain)
    for fname, v_tupels, pos_tupels in traindata_iterator:

        assert len(pos_tupels) > 1
        for tupel in pos_tupels:
            timestamp = tupel[0]
            value = tupel[1]
            assert timestamp != None
            assert value != None

def test_english_pos_tupels():
=======
def test_pos_tupels():
>>>>>>> 3480e95... reformatted test training file
    """
    Are all pos tier tupels created without None values?
    :return:
    """
    traindata_iterator = corpustools.ExmaTokenPOSIterator(englishExmaraldaTrain)
    for fname, v_tupels, pos_tupels in traindata_iterator:

        assert len(pos_tupels) > 1
        for tupel in pos_tupels:
            timestamp = tupel[0]
            value = tupel[1]
            assert timestamp != None
            assert value != None


<<<<<<< HEAD
def test_german_tokenpos():
    trdata = corpustools.ExmaTokenPOSIterator(germanExmaraldaTrain)
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

def test_english_tokenpos():
    trdata = corpustools.ExmaTokenPOSIterator(englishExmaraldaTrain)
=======
def test_tokenpos():
    trdata = corpustools.make_tier_tuple_list(tdata)
>>>>>>> 3480e95... reformatted test training file
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

<<<<<<< HEAD
    assert len(trfiles) == counter



# create_tagger_trainingfile(germanExmaraldaTrain, german_tt_trainfile)

# assert create_tagger_trainingfile(englishExmaraldaTrain, english_tt_trainfile)

=======
    assert len(trfiles) == counter
>>>>>>> 3480e95... reformatted test training file
