import logging
import os
from lxml import etree

XML_PARSER = etree.XMLParser()


def extract_v_student(documenttree):
    """
    :param document:
    """
    vtier = None
    for element in documenttree.iter('tier'):
        if len(element.get('display-name').split()[0]) >= 3 and element.get('category') == 'v':
            vtier = element
    return vtier


class ExmaIterator(object):
    """
    exmaralda file iterator
    Each parsed document is represented by a (filename, list of sentences) tuple.
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
        return file_name, extract_v_student(tree)
