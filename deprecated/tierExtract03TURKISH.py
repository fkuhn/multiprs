#REVISED VERSION OF THE TIER-EXTRACT SCRIPT OCT 2013
#AUTHOR F KUHN
"""
tierExtract v3.0 - Oktober 2013
Multilit Project
Institute for German Studies
University of Potsdam
Author: Florian Kuhn

extracts verbal tiers of interviewed students from an exmaralda-file.
the tiers are saved in an txt file.
"""

#import section
import sys
import os
import re
import codecs
import string
from lxml import etree as ET





####################################

#method definitions

#open an .exb filelist and etree.parse it and return a list of parsed docs
def parse_exmaralda(filelist):
    parsed_docs = []
    #4a. iterate over all files in the exmafilelist
    for fichier in filelist:
        try:
            #4b. open a file in fich with utf8 encoding and append it to docs
            fich = codecs.open(fichier, encoding='utf-8')
            parsed_docs.append(fich)
        except:
            print "file error: " + fichier
            continue
            #4c. return docs
    return parsed_docs


# def extractTierByCategory(document, pattern, category):
# #6a. define a vtier variable
#     vtier = None
#     #6b. regex search for the pattern in attribute 'display-name' of every tier in doc AND check if category matches
#     for element in document.iter('tier'):
#         if re.search(pattern, element.get('display-name')) and element.get('category') == category:
#             vtier = element
#     return vtier


def extract_v_student(document):
    """

    :param document:
    """
    try:
        parsed_document = ET.parse(document)
    except:
        print "element tree parse error: " + document

    vtier = None
    for element in parsed_document.iter('tier'):
        if len(element.get('display-name').split()[0]) >= 3 and element.get('category') == 'v':
            vtier = element
    return vtier

###########
#main script body
###########

#1. read command line parameter
directory = ""
try:
    directory = sys.argv[1]
except:
    print "Parameter used wrong"

# 2. write filelist in directory to exmafilelist
exmafilelist = os.listdir(directory)
# 3. then change working directory to 'directory'
os.chdir(directory)
# 4. parse the exmafilelist (see method definition)
doclist = parse_exmaralda(exmafilelist)
# 5. define vtierlist for the v tier of the student. contains 2tuple of (docname,vtier)
vtierlist = []
# 6. parse every doc with etree. and extract the student v tier from it. append it to vtierlist

# content is the tuple mentioned in 5.
for doc in doclist:
    try:
        vtierlist.append((doc.name, extract_v_student(doc)))
    except:
        print "parse error in file: " + doc.name
        continue

for e in vtierlist:
    print e

os.chdir('../')

for vtiertupel in vtierlist:
    #7. open an output-file object for every vtiertupel.
    vfile = codecs.open('Korpus_tuerkischOUT/' + vtiertupel[0] + '_V.txt', 'w', encoding='utf-8')
    #TODO REMOVE HARDCODED OUTPUTFOLDER!
    #8. iterate over all tokens in the v tier and write them to vfile. moreover,
    # add the timestamp-tag at the beginning of each line
    #this tag will be ignored by the tagger and is used to align the POS Tag later on
    try:
        for velem in vtiertupel[1]:
            if velem is not None:
                try:
                    vfile.write('<' + velem.get('start') + ' ' + velem.get('end') + '>' + '\t' + velem.text + '\n')
                except:
                    print velem + " is not valid"
                    continue
    except:
        print "file error: " + vtiertupel[0]
        continue
        #close the file opened at (7)
        file.close()
