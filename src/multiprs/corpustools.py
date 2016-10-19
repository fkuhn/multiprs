from __future__ import unicode_literals
import logging
import os
from lxml import etree

# constants definition
XML_PARSER = etree.XMLParser()
TAB = '\t'
LBREAK = '\n'


logging.basicConfig(level=logging.WARNING)

def write_meta2exma(corpuspath):
    """
    writes metadata of a speaker to all
    corresponding exmaralda files in a directory
    :return:
    """
    pass


def extract_v_student(documenttree):
    """
    :param documenttree: etree object
    :returns vtier: verbal exmaralda tier
    """
    vtier = None
    for element in documenttree.iter('tier'):
        if len(element.get('display-name').split()[0]) >= 3 and element.get('category') == 'v':
            vtier = element
    return vtier


def extract_pos_student(documenttree):
    """
    :param documenttree: etree object
    :returns postier exmaralda tier
    """
    postier = None
    for element in documenttree.iter('tier'):
        if len(element.get('display-name').split()[0]) >= 3 and element.get('category') == 'POS':
            postier = element

    return postier


def timestamp_token_tupler(verbaltier):
    """
    takes an exmaralda verbal tier and returns a
    list of (<timestamp>, token) tuples.
    :param verbaltier: list
    :returns timed_vlist: list
    """
    timed_vlist = list()
    if verbaltier is None:
        return None
    for velem in verbaltier:
        if velem is not None:
            try:
                timed_vlist.append(('<' + velem.get('start') + ' ' + velem.get('end') + '>' + '\t',
                                        unicode(velem.text)))
            except TypeError:

                print velem + " is not valid"
                continue
    return timed_vlist



class ExmaTimeStampTokenIterator(object):
    """
    exmaralda file iterator
    takes an exmaralda source folder and returns an
    """
    def __init__(self, corpus_path):
        self.corpus_path = os.path.abspath(corpus_path)
        self.file_names = iter(os.listdir(self.corpus_path))

    def __iter__(self):
        return self

    def next(self):
        file_name = self.file_names.next()

        try:
            tree = etree.parse(os.path.join(self.corpus_path, file_name), parser=XML_PARSER)
        except AssertionError:
            logging.error('Assertion Error. No Root: ' + file_name)
            return

        vtier = extract_v_student(tree)

        return file_name, timestamp_token_tupler(vtier)


class CorpusIterator(object):
    """
    exmaralda file iterator
    takes an exmaralda source folder and returns
    filename and elementree
    """
    def __init__(self, corpus_path):
        self.corpus_path = os.path.abspath(corpus_path)
        self.file_names = iter(os.listdir(self.corpus_path))

    def __iter__(self):
        return self

    def next(self):
        file_name = self.file_names.next()

        try:
            tree = etree.parse(os.path.join(self.corpus_path, file_name), parser=XML_PARSER)
        except AssertionError:
            logging.error('Assertion Error. No Root: ' + file_name)
            return

        # vtier = extract_v_student(tree)

        return file_name, tree

class CorpusIteratorVTier(object):
    """
    exmaralda file iterator
    takes an exmaralda source folder and returns
    the student's verbal tier of the file parsed as
    etree element.
    """
    def __init__(self, corpus_path):
        self.corpus_path = os.path.abspath(corpus_path)
        self.file_names = iter(os.listdir(self.corpus_path))

    def __iter__(self):
        return self

    def next(self):
        file_name = self.file_names.next()

        try:
            tree = etree.parse(os.path.join(self.corpus_path, file_name), parser=XML_PARSER)
        except AssertionError:
            logging.error('Assertion Error. No Root: ' + file_name)
            return

        vtier = extract_v_student(tree)

        return file_name, vtier


class ExmaTokenPOSIterator(object):
    """
    exmaralda file iterator
    takes an exmaralda source folder and returns a filename and all
    student vtier POS, TOKEN tuples per file
    """
    def __init__(self, corpus_path):
        self.corpus_path = os.path.abspath(corpus_path)
        self.file_names = iter(os.listdir(self.corpus_path))

    def __iter__(self):
        return self

    def next(self):
        file_name = self.file_names.next()

        try:
            tree = etree.parse(os.path.join(self.corpus_path, file_name), parser=XML_PARSER)
            if not hasattr(tree, '__iter__'):
                return
        except AssertionError:
            logging.error('Assertion Error. No Root: ' + file_name)
            return

        vtier = extract_v_student(tree)
        postier = extract_pos_student(tree)

        if vtier == None:
            return
        elif postier == None:
            return

        return file_name, timestamp_token_tupler(vtier), timestamp_token_tupler(postier)



def make_tier_tuple_list(resourcepath):
    """
    same funtionality liek ExmaTokenPOSIterator
    but with using a simple list-returning function
    :param resourcepath:
    :return:
    """
    corpus_path = os.path.abspath(resourcepath)
    file_names = os.listdir(corpus_path)
    results = list()
    for file_name in file_names:
        try:
            tree = etree.parse(os.path.join(corpus_path, file_name), parser=XML_PARSER)
        except AssertionError:
            logging.error('Assertion Error. No Root: ' + file_name)

        vtier = extract_v_student(tree)
        ptier = extract_pos_student(tree)

        # results.update({file_name: (timestamp_token_tupler(vtier), timestamp_token_tupler(ptier))})

        ts_vtier = timestamp_token_tupler(vtier)
        ts_ptier = timestamp_token_tupler(ptier)

        if ts_ptier == None:
            logging.warning('Skipping file...{} No pos tier parsed'.format(file_name))
            continue
        if ts_vtier == None:
            logging.warning('Skipping file...{} No verbal tier parsed'.format(file_name))
            continue

        result = file_name, ts_vtier, ts_ptier
        results.append(result)

    return results




class ExmaTrainData(object):
    """
    Training Data of a directory
    """

    def __init__(self, train_data_path):
        self.train_path = os.path.abspath(train_data_path)
        self.filecount = len(os.listdir(self.train_path))
        self._tokenpositer = ExmaTokenPOSIterator(self.train_path)
        self.text = self._prepare_train_data(self.train_path)

    def _prepare_train_data(self, datapath):
        """
        takes path to a directory of train data and returns
        a single plaintext file of token \t postag per line
        """
        data = list()

        for filename, tokens, poses in self._tokenpositer:
            for tokenpos in tokens, poses:
                data.append('{}{}{}{}'.format(tokenpos[1], TAB, tokenpos[1], LBREAK))
        textstring = ''.join(data)

        return textstring
