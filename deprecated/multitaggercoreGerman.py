import MultilitCorpusClasses
import corpusMethods

__author__ = 'fkuhn'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#! /usr/bin/python

#########
#IMPORTS#
#########

import sys, os, re

#import generic modules
#import etree
from lxml import etree

###########
#*MAIN BODY#
###########
#1. read command line paraer
directory = None
tmpdir = "pos"
#a local output directory
try:
    directory = sys.argv[1]
    corpusdir = sys.argv[2]
except IndexError:
    print "Parameter used wrong"
#2. write filelist in directory to inputfilelist
inputfilelist = os.listdir(directory)
#print inputfilelist
#3. then change working directory to 'directory'
os.chdir(directory)
#4. tree tag all files in the directory
for f in inputfilelist:
    #subprocess.call("sh ../taggerscript/tree-tagger-multi_german.sh "+f+" > "+f+".pos")
    #writes output to a file with suffix .pos
    os.system("sh ../taggerscript/tree-tagger-multi_german.sh " + f + " > " + tmpdir + "/" + f + ".pos")
tmpfilelist = os.listdir(tmpdir)
os.chdir(tmpdir)
#read the tagged data and store it in a tuple list

processedTaggedFiles = []
#a list to store all PosTagContainer-Objects

for fi in tmpfilelist:
    posdat = corpusMethods.read_tagged_data(fi)
    tupelliste = []
    tmplist = []
    tupelliste.append(fi.split('.')[0])
    #append the filename to the tupellist and use split to remove any extension
    global tmplist
    for x in range(0, len(posdat) - 1):
        #define length of posdat minus 1 (because loop starts with 0)
        if re.search('^<T.*', posdat[x]):
            #just accepting when a line-element in tupelliste begins with a timestamp. else continue with next item
            tmplist = [posdat[x]]
            tupelliste.append(tmplist)
        else:
            try:
                tmplist.append(posdat[x].split()[1])
            except:
                continue
                #store the pos tag
    pstgcon = MultilitCorpusClasses.PosTagContainer(tupelliste)
    processedTaggedFiles.append(pstgcon)

#testprint
#for i in ProcessedTaggedFiles:
#	print i.get_filename()
#	print i.get_timepos()
# :)
###########################################
#READ IN CORPUSFILE AS PARSED ETREE-OBJECTS
###########################################
os.chdir('../../')
corpfilelist = os.listdir(corpusdir)
corpus = []
os.chdir(corpusdir)
for cf in corpfilelist:
    corpus.append(MultilitCorpusClasses.CorpusFileEtree(cf))

###########################################
#MATCH POSTAG OBJECT AND ETREE OBJECTS x
###########################################
corpusmatches = []
for pt in processedTaggedFiles:
    for et in corpus:
        if pt.filename == et.filename:
            corpusmatches.append((et, pt))
#print corpusmatches #contains tupels of matched object

#####################################
#GENERATE AN EVENT TAG FROM POS INFO x
#####################################
#<event start="T20" end="T21">POS </event>

#for i in processedTaggedFiles:
#	print i.events

####################################################
#GENERATE A MATCHING TIER TAG AND INCLUDE EVENT TAGS
####################################################
#iterate over all tupel with matched exmafiles and postagfiles


def extract_tier_by_name(document, pattern):
    #6a. define a vtier variable
    vtier = None
    #6b. regex search for the pattern in attribute 'display-name' of every tier in doc AND check if category matches
    for element in document.iter('tier'):
        if re.search(pattern, element.get('display-name')):
            vtier = element
    return vtier

##########################
#
#########################

for tupel in corpusmatches:

    displayname = corpusMethods.extract_display_name(tupel[0].eltree)
    tnumber = 'TIE' + str(len(tupel[0].eltree.find('basic-body')))
    postier = etree.Element('tier')
    postier.set("id", tnumber)
    postier.set("category", "POS")
    postier.set("type", "a")
    postier.set("display-name", displayname.split()[0] + " [pos]")

    ############################################
    ###########################################
    #Module for parameters to ignore
    ###########################################
    #longpause = re.compile("\(\([0-9]+,[0-9]+s\)\)")
    #re.search(ur'\(\([0-9]+,[0-9]+s\)\)', ev.text, re.UNICODE):
    #interpunctions to ignore
    #tilgen der selbstkorrektur tags...

    for ev in tupel[1].events:

        if re.search(ur'([A-Z]+[1-3])(W)?(SK)?', ev.text, re.UNICODE):
            m = re.search(ur'([A-Z]+[1-3])(W)?(SK)?', ev.text, re.UNICODE)
            #Alle Eintraege mit *SK entfernen. Bei *W das POS-Tag mit W endend ignorieren.

        if ev.text == "PAUSE":
            ev.text = ""
            postier.append(ev)
        if ev.text == ".$":
            ev.text = ""
            postier.append(ev)
        if ev.text == ",$":
            ev.text = ""
            postier.append(ev)
            postier.append(ev)
        if ev.text == "!$":
            ev.text = ""
            postier.append(ev)
        if ev.text == "?$":
            ev.text = ""
            postier.append(ev)
        if ev.text == "/$":
            ev.text = ""
            postier.append(ev)
        if ev.text == "@$":
            ev.text = ""
            postier.append(ev)
        if ev.text == "//$":
            ev.text = ""
        else:
            postier.append(ev)
            #this works
    tupel[0].eltree.find('basic-body').append(postier)
    #access the elementtree

#after the last existing tier element, insert a new tier element containing the pos data

os.chdir('../')

for tupel in corpusmatches:
    tupel[0].eltree.write('testoutputGERMAN/' + tupel[0].filename + '_pos.exb')

###############
#END OF MODULE#
###############

