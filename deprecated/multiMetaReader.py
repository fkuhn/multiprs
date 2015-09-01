#!/usr/bin/env python
# -*- coding: utf-8 -*-

#! /usr/bin/python

"""
Reads data from the survey .xls file and writes it to the appropiate exmaralda file
"""

import sys

import xlrd
import xlutils

#generic modules
from src import metasurvey

surv = metasurvey.Survey()
surveydict = {}  #dictionary fuer den survey-sheet
#orndung:
#A1..Z1 = spaltennamen 
#idee: A2..An identifier fuer schueler im korpus --> key fuer dictionary
#die werte einer zeile bis auf An werden in ein tupel geschrieben




#++++++++++++++++++++++++++
#++++PRIMARY FUNCTION++++++
#++++++++++++++++++++++++++
#the corpus keyword is the first entry in a row. its a unique identifier denoting the student refered to

def readSurvey(ssheet):
    survey_sheet = ssheet
    survey_object = metasurvey.Survey()  #define generic survey object
    #datum = metasurvey.Entry()
    datum = None
    for row_index in range(survey_sheet.nrows):
        #datum = metasurvey.Entry() #define a new Entry
        #print "Row #"+str(row_index)
        if row_index > 0:  #check if the refered item is not just the index-integer of the table

            datum = metasurvey.Entry(survey_sheet.cell_value(row_index, 0).encode(
                'utf-8'))  #create an entry instance with its corpus keyword

            for col_index in range(survey_sheet.ncols):
                #datum = metasurvey.Entry() #define a new entry object for each row
                #print str(col_index) + ' ' + survey_sheet.cell_value(row_index,col_index).encode('utf-8') #TODO testoutput
                #print "Corpuskey: " + survey_sheet.cell_value(row_index,col_index).encode('utf-8')

                if col_index > 0 and (type(survey_sheet.cell_value(row_index, col_index)) is str):
                    datum.addData(survey_sheet.cell_value(row_index, col_index).encode('utf-8'))
                elif col_index > 0:
                    datum.addData(survey_sheet.cell_value(row_index, col_index))

            survey_object.add
    return survey_object


#tiny function to make tuples 
def make_tuple(variables, names):
    return tuple(variables[n] for n in names)


#TODO:
def to_dict(sheet):
    for row_index in range(sheet.nrows):  #for each row
        for col_index in range(sheet.ncols):
            print ""


def introspect_surveysheet(sheet):
    print sheet.name
    print sheet.nrows
    print sheet.ncols
    for row_index in range(sheet.nrows):
        for col_index in range(sheet.ncols):
            print xlrd.cellname(row_index, col_index), '-',  #nur den index-namen einer zelle e.g. A1 B4 etc.
            print sheet.cell(row_index, col_index).value  #wert einer zelle e.g. 'steuer'
    return


def browse_column(sheet, c_index):
    print sheet.name


#read the command line arguments
#1. surveyfile
#2. corpusfolder containing multilit-exmaralda files
try:
    surveyfile_object = xlrd.open_workbook(sys.argv[1])  #open the file as xlrd-fileobject
#corpusfolder = sys.argv[2]

except:
    print "wrong parameters"
    sys.exit()

surveyfile_worksheets = surveyfile_object.sheet_names()



#process the worksheets

#read out the corpus-pseudonyms
ss = readSurvey(surveyfile_object.sheet_by_index(0))
print ss
ss.getCorpusKeys()
