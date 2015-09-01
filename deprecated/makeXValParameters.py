__author__ = 'fkuhn'

import sys
import os

corpusdirectory = sys.argv[1]

os.chdir(corpusdirectory)

alldoc = corpusdirectory + '/all'

first = corpusdirectory + '/1'
second = corpusdirectory + '/2'
third = corpusdirectory + '/3'


def maketrainlist(valdir):
    """
    make a list that contains all files but the ones to be evaluated....
    """
    trainlist = []

    valdir = os.listdir(valdir)
    for i in alldoc:
        if i not in valdir:
            trainlist.append(i)
    return trainlist


for element in os.listdir(corpusdirectory):
    if element in [0 - 9]:
        trainlist = maketrainlist(element)

print trainlist
