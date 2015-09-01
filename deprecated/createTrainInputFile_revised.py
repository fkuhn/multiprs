#!/usr/bin/env python

# -*- coding: utf-8 -*-
# 1st argument: directory containing manual pos-tagged .exb files

#IMPORTS
import os
import re
import codecs
import string

from lxml import etree as ET
#generic imports
from corpusFileTagPreProcessor import ValidTags

# "This script extracts v and POS tier of the interviewed person (denoted by a three letter abbreviation)
# and aligns it according to the common timeline of the exmaralda source file.\n"
#"Alignment is realised by taking a POS event element and searching for its v event element equal,
# since v event elements include irrelevant interview introduction clutter that has not been pos tagged.\n"
#define methods to read word-pos tupel

####################
#METHOD DEFINITIONS#
####################

def parse_exmaralda(filelist):
    """
    simply parses the files given in the list and returns
    a list of etree-parsed objects of these files.
    @param filelist:
    @return: docs
    """
    docs = []
    for fichier in filelist:
        #fich = codecs.open(fichier, encoding='utf-8-sig')
        fich = codecs.open(fichier, encoding='utf-8')
        docs.append(ET.parse(fich))
    return docs


def extract_v_pos(document, pattern, pos_category, v_category):
    """
    extracts v tier and pos tier of current exmaralda document
    @param document:
    @param pattern:
    @param category1:
    @param category2:
    @return: tier_tupel
    """
    tier_tupel = ()
    #extract v and pos tier, the 2 relevant tiers
    for element1 in document.iter('tier'):

        if re.search(pattern, element1.get('display-name')) and element1.get('category') == pos_category:

            for element2 in document.iter('tier'):

                if re.search(pattern, element2.get('display-name')) and element2.get('category') == v_category:
                    #found a matching tupel: write it to the tier_tupel list
                    tier_tupel = (element1, element2)

    return tier_tupel


def find_startevent(s, p, v):
    """
    looks for the startevent
    @param p:
    @param v:
    """
    postier = p
    vtier = v
    #process index and item with enumerate
    for eventv_index, eventv in enumerate(vtier):
        #find the beginning of the pos tier
        if int(string.lstrip(eventv.get('start'), 'T')) == int(
                string.lstrip(postier[0].get('start'), 'T')):
            #startvalue must be equal or more

            return eventv_index
    return None


def align_tier_events(ttl):
    """
    a tiertupel list
    @param ttl:
    @return: alignment_list
    """
    alignment_list = []
    #aus = open ('../')
    #takes a tupel of pos and v event-tiers and alignes them.

    for tupel in ttl:

        try:
            pos_start = string.lstrip(tupel[0][0].get('start'), 'T')
            #get the first tupel element and its first element's value

            start_elementv_index = int(find_startevent(int(pos_start), tupel[0], tupel[1]))
        except:

            print >> sys.stderr, "error finding startevent"
            print >> sys.stderr, "fehler: " + it_v[0].text + ' ' + it_pos[0].text

        start_elementv_index -= 1

        posindex = 0
        try:
            it_v = tupel[1]
            it_pos = tupel[0]
        except:
            continue
        #for every tier tupel align their v and pos tokens

        try:
            alignment_list.append(check_start_time_it(it_v, it_pos))
        except:
            print >> sys.stderr, "error checking startime"

    return alignment_list


def check_start_time_it(tierv, tierpos):
    """
    check the start time of both tiers (v and pos)
    @param tierv:
    @param tierpos:
    @return: returntupellist
    """
    #iterative method
    returntupellist = []
    for eventv in tierv:
        for eventpos in tierpos:
            if int(string.lstrip(eventv.get('start'), 'T')) == int(string.lstrip(eventpos.get('start'), 'T')):
                returntupellist.append((eventv.text, eventpos.text))

                break

    return returntupellist


###########
#MAIN BODY#
#SCRIPT STARTING HERE#
###########

#usage: python createTrainInputFile.py annotatedfilesdir validtagsfilename

#main function


def make_input_file(annofiledir, validtagsfilename, traininputfilename):
    workdir = os.getcwd()
    ##read command line parameter
    #annofiledir = sys.argv[1]
    #validtagsfilename = sys.argv[2]
    #traininputfilename = sys.argv[3]

    #a list of remark suffixes
    remark_suffixes = ["SK", "W"]

    #define validtags object
    vtags = ValidTags(validtagsfilename, remark_suffixes)

    #write filelist in directory to afdlist
    afdlist = os.listdir(annofiledir)

    print >> sys.stderr, "Reading directory " + annofiledir + "\n"
    #change working directory
    os.chdir(annofiledir)

    doclist = parse_exmaralda(afdlist)
    #define a tier tuple list
    ttl = []
    for doc in doclist:
        ttl.append(extract_v_pos(doc, '^[A-Z]{3,} ', 'POS', 'v'))

    #make an output list for the training file.
    output_list = align_tier_events(ttl)

    #########################
    #WRITE THE TRAINING FILE#
    #########################

    #open an output-file object m
    #set back working directory
    os.chdir(workdir)
    #trainingfile = codecs.open(traininputfilename, 'w', encoding='utf-8-sig')
    trainingfile = codecs.open(traininputfilename, 'w', encoding='utf-8')

    filenumber = 0
    tokenposnumber = 0

    for tupellist in output_list:
        filenumber += 1
        for tupel in tupellist:
            #Important: Strip trailing whitespaces to prevent empty tag error during training.
            token = tupel[0].strip()
            pos = tupel[1].strip()
            if token and pos:
                #check if pos tag is valid and write to outputfile
                #else do not write anything
                try:
                    if vtags.is_valid_postag(pos):

                        #trainingfile.write(tupel[0] + '\t' + vtags.get_nearest_tag(tupel[1]) + '\n')
                        #pos = tupel[1]
                        pos = vtags.del_remarks(pos)
                        trainingfile.write(token + '\t' + pos + '\n')

                    else:
                        if vtags.is_valid_postag_composite(pos):
                            #trainingfile.write(tupel[0] + '\t' + vtags.get_nearest_tag(tupel[1]) + '\n')
                            trainingfile.write(token + '\t' + pos + '\n')
                except:
                    print sys.stderr, tupel[1]
            tokenposnumber += 1

    trainingfile.close()

    print >> sys.stderr, "script terminated with " + str(filenumber) + " files processed and " + str(
        tokenposnumber) + " (token,postype) tupel written to " + traininputfilename
    ###############
    #END OF MODULE#
    ###############


import sys

make_input_file(sys.argv[1], sys.argv[2], sys.argv[3])
