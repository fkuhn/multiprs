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

    def get_speaker(self, sigle):
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

            #speaker_label = self.metasheet.cell(row_index, 0).value
            #speaker_row = self.metasheet.row_values(row_index)
            spk = {}
            for i in speaker_row:
                spk.update({self.labels[speaker_row.index(i)]: i})
            speaker.update({speaker_row[0]: spk})
            speakersdata.update(speaker)
        return speakersdata

    def insert_metadata(self, corpuspath):
        """
        inserts matching metadata sets into all exmaralda files of a given directory
        :param corpuspath: a path to a directoy w/ a collection of exb files
        :return:
        """
        # corpuspath = os.path.abspath(corpuspath)
        filelist = os.listdir(corpuspath)
        exmafiles = corpustools.CorpusIterator(corpuspath)


        for speaker in self.studspeakers:
            for exmafilename, exmatree in exmafiles:
                speakers = exmatree.xpath('/basic-transcription/head/speakertable/speaker')
                for speaker in speakers:
                    pass


#class Comafile:
    ##<Speaker Id="SID5A1794D5-D320-86FC-9248-4D9BF8B8DE7D">
    ## <Sigle>ALP</Sigle>
    ## <Pseudo>ALP</Pseudo>
    ##<Sex>male</Sex>
    ##<Description>
    ##<Key Name="id">SPK0</Key>
    ##<Key Name="@abbreviation">ALP</Key>
    ##<Key Name="id0">SPK1</Key>
    ##</Description>
    ## </Speaker>

    #def __init__(self, cfile):

        #self.cparse = etree.parse(cfile)
        #self.transkription_name = self.cparse.find('transcription-name')

    #def write_speaker_to_coma(self, spktuple):
        #"""
        #writes metadata dictionary of a speaker to comasurvey = xlrd.open_workbook(tablefile)

        #"""
        #for speaker in self.cparse.iter('Speaker'):
            #try:
                #if speaker.find('Sigle').text == spktuple[0]:
                    ##write all metadata to description tag
                    #desc = speaker.find('Description')

                    #for i in spktuple[1].iteritems():
                        #s = etree.SubElement(desc, 'Key', {'Name': i[0]})
                        #s.text = str(i[1])
            #except:
                #continue
        #return

    #def write_xml(self, f):
        #return self.cparse.write(f, encoding="utf-8")

    #def speakers(self):

        #sp = []

        #for speaker in self.cparse.iter('Speaker'):
            #try:
                #if len(speaker.find('Sigle').text) == 3:
                    #sp.append(speaker.find('Sigle').text)
            #except:
                #continue
        #return sp


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

#def add_coma_speaker_description(speaker):



#MAIN
#surv = read_table('Metadata/Fragebogen_SEK_14_3_2013.xls')

#cm = Comafile('Coma/MultilitGer.coma')

#sp = cm.speakers()

#print sp
#print "Number of Speakers: " + str(len(sp))

#for person in sp:
#    speak = find_speaker(person, surv.sheet_by_index(0))
#    cm.write_speaker_to_coma(speak)

#print cm.write_xml('MetaMultiGer.coma')

