#!/usr/bin/env python
# -*- coding: utf-8 -*-

#! /usr/bin/python

"""
classes used in processing the multilit corpus
"""

from lxml import etree
import codecs


class PosTagContainer:
    """
    this class is a container for all pos-tag relevant informations.
    """

    def __init__(self, plist):
        self.filename = plist[0]
        #store the filename
        self.timepos = plist[1:]
        #store all timestamp-postag sublists in 'timepos'
        self.events = self.get_event(self.timepos)
        #generate a list of events

    def get_filename(self):
        return self.filename

    def get_timepos(self):
        return self.timepos

    def get_event(self, tlist):
        #returns a list of events
        evlist = []
        for i in tlist:
            try:
                ev = etree.Element("event")
                #create event etree elements
                ev.set("start", i[0].split()[0].strip('<'))
                ev.set("end", i[0].split()[1].strip('>'))
                ev.text = i[1]
                evlist.append(ev)
            except:
                continue
        return evlist


class CorpusFileEtree:
    """
    TOFO:
    a single corpus object
    """

    def __init__(self, file):
        self.filename = file.split('.')[0]
        self.eltree = self.parse_exmaralda(file)
        #the elementree object of the content

    def parse_exmaralda(self, fi):
        fich = codecs.open(fi, encoding='UTF-8')
        return etree.parse(fich)
