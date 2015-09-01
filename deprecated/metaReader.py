__author__ = 'fkuhn'

import xlrd
#http://www.python-excel.org/
from lxml import etree


class Comafile:
    #<Speaker Id="SID5A1794D5-D320-86FC-9248-4D9BF8B8DE7D">
    # <Sigle>ALP</Sigle>
    # <Pseudo>ALP</Pseudo>
    #<Sex>male</Sex>
    #<Description>
    #<Key Name="id">SPK0</Key>
    #<Key Name="@abbreviation">ALP</Key>
    #<Key Name="id0">SPK1</Key>
    #</Description>
    # </Speaker>

    def __init__(self, cfile):

        self.cparse = etree.parse(cfile)
        self.transkription_name = self.cparse.find('transcription-name')

    def write_speaker_to_coma(self, spktuple):
        """
        writes metadata dictionary of a speaker to coma
        """
        for speaker in self.cparse.iter('Speaker'):
            try:
                if speaker.find('Sigle').text == spktuple[0]:
                    #write all metadata to description tag
                    desc = speaker.find('Description')

                    for i in spktuple[1].iteritems():
                        s = etree.SubElement(desc, 'Key', {'Name': i[0]})
                        s.text = str(i[1])
            except:
                continue
        return

    def write_xml(self, f):
        return self.cparse.write(f, encoding="utf-8")

    def speakers(self):

        sp = []

        for speaker in self.cparse.iter('Speaker'):
            try:
                if len(speaker.find('Sigle').text) == 3:
                    sp.append(speaker.find('Sigle').text)
            except:
                continue
        return sp


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
    #   print sheet.name
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
surv = read_table('Metadata/Fragebogen_SEK_14_3_2013.xls')

cm = Comafile('Coma/MultilitGer.coma')

sp = cm.speakers()

print sp
print "Number of Speakers: " + str(len(sp))

for person in sp:
    speak = find_speaker(person, surv.sheet_by_index(0))
    cm.write_speaker_to_coma(speak)

print cm.write_xml('MetaMultiGer.coma')

