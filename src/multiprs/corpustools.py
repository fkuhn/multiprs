import logging
import os
from lxml import etree

XML_PARSER = etree.XMLParser()


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


def timestamp_token_tupler(verbaltier):
    """
    takes an exmaralda verbal tier and returns a
    list of (<timestamp>, token) tuples.
    :param verbaltier: list
    :returns timed_vlist: list
    """
    timed_vlist = list()

    for velem in verbaltier:
        if velem is not None:
            try:
                timed_vlist.append(('<' + velem.get('start') + ' ' + velem.get('end') + '>' + '\t',
                                        unicode(velem.text) + '\n'))
            except TypeError:

                print velem + " is not valid"
                continue
    return timed_vlist


class ExmaIterator(object):
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

        return file_name, tree

