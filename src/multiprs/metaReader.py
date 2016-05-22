from __future__ import print_function, unicode_literals
import xlrd
# http://www.python-excel.org/
from lxml import etree
import os
import corpustools


class MetaTableSpeakers(object):
    """
    Iterator class returning an metadata table instance
    """
    def __init__(self, metafile):
        self.metaworkbook = xlrd.open_workbook(metafile)
        self.metasheet = self.metaworkbook.sheet_by_index(0)
        self.labels = self.metasheet.row_values(0)
        self.studspeakers = self._find_speakers()

    def get_speaker_metadata(self, sigle):
        """
        returns a dictionary of speaker attributes given a speaker sigle
        :param sigle: string
        :return: dictionary
        """
        if sigle in self.studspeakers.keys():
            return self.studspeakers.get(sigle)
        else:
            return None

    def _find_speaker(self, spkname):
        """
        searches for a speaker and returns her/his metadata entry
        """
        spk = {}
        for row_index in range(self.metasheet.nrows):
            if self.metasheet.cell(row_index, 0).value == spkname:
                speaker_row = self.metasheet.row_values(row_index)
                for i in self.labels:
                    spk.update({i: speaker_row[self.labels.index(i)]})

        return {spkname: spk}

    def _find_speakers(self):

        speakersdata = {}

        attributes = self.labels
        # iterate over rows, start with index 1 to omit first header-row.
        for row_index in range(1, self.metasheet.nrows):

            speaker = {}
            speaker_row = self.metasheet.row_values(row_index)

            # speaker_label = self.metasheet.cell(row_index, 0).value
            # speaker_row = self.metasheet.row_values(row_index)
            spk = {}
            for i in speaker_row:
                spk.update({self.labels[speaker_row.index(i)]: i})
            speaker.update({speaker_row[0]: spk})
            speakersdata.update(speaker)
        return speakersdata

    def insert_metadata(self, corpuspath, outputpath):
        """
        inserts matching metadata sets into all exmaralda files of a given directory
        :param corpuspath: a path to a directoy w/ a collection of exb files
        :param outputpath: path where the modified exb are written
        :param debug: boolean. flag to generate debugging logging info
        :return: list of modified etree objects
        """

        if os.path.isdir(os.path.abspath(outputpath)) and os.path.isdir(os.path.abspath(corpuspath)):

            # corpuspath = os.path.abspath(corpuspath)
            filelist = os.listdir(corpuspath)
            exmaiter = corpustools.CorpusIterator(corpuspath)
            modfiles = []

            for filename, exmatree in exmaiter:
                infile_speakers = exmatree.xpath('/basic-transcription/head/speakertable/speaker')
                for infile_speaker in infile_speakers:
                    try:
                        infile_speaker_label = infile_speaker.find("abbreviation").text
                    except AttributeError:
                        continue
                    if self.get_speaker_metadata(infile_speaker_label):
                        infile_speaker_data = self.get_speaker_metadata(infile_speaker_label)
                        for key, value in infile_speaker_data.items():
                            # iterate over tuples of key,values
                            udspeaker = infile_speaker.find('ud-speaker-information')
                            udinfo = etree.SubElement(udspeaker, "ud-information")
                            udinfo.set("attribute-name", key)
                            udinfo.text = "{}".format(value)
                output = etree.tostring(exmatree)
                with open(os.path.join(outputpath, filename), 'w') as out:
                    out.write(output)


class Speaker:
    def __init__(self):
        self.sigle = ""
        self.pseudo = ""
        self.sex = ""
        self.description_dictionary = {}

    def add_key_value(self, k, v):
        self.description_dictionary.update({k: v})


#FUNCTIONS
def find_speaker(spkname, surveysheet):
    """
    searches for a speaker and returns her/his metadata entry
    """
    spk = {}
    labels = surveysheet.row_values(0)
    for row_index in range(surveysheet.nrows):
        if surveysheet.cell(row_index, 0).value == spkname:
            speaker_row = surveysheet.row_values(row_index)
            for i in labels:
                spk.update({i: speaker_row[labels.index(i)]})

            return (spkname, spk)


def read_table(tablefile):
    """
    reads an metadata-excel table
    """
    #read in a workbook from file
    survey = xlrd.open_workbook(tablefile)

    #for sheet in survey.sheets():

    #   print sheet
    #   print sheet.namesurvey = xlrd.open_workbook(tablefile)

    #   print "Number of rows: "+str(sheet.nrows)
    #   print "Number of columns: "+str(sheet.ncols)
    return survey


def read_coma_file_speakers(cfile):
    """
    read all speakers of a coma file.
    """
    comaf = etree.parse(cfile)

    return comaf
