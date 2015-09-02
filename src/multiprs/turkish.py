import treetaggerwrapper
import corpustools
import os
import argparse


# note: TreeTagger must be installed on your system
# turkish parameter file must be in default treetagger lib dir

PARFILENAME = 'TurkishAPR10.par'


# tree tagger configuration

turktagger = treetaggerwrapper.TreeTagger()
turktagger.lang = 'tr'
parpath = turktagger.taglibdir
turktagger.tagparfile = os.path.join(parpath, PARFILENAME)


def prepare_iterator(corpuspath):
    """
    extracts
    :param corpuspath:
    :return:
    """
    timed_token_iterator = corpustools.ExmaIterator(corpuspath)
    return timed_token_iterator


def pos_tag_directory(corpuspath):

    t_iterator = prepare_iterator(corpuspath)
    for timeline in t_iterator:

        pos_tag_turkish_vtier(timeline)



def main():
    """
    main method for turkish pos tagging
    :return:
    """


def pos_tag_turkish_vtier(timelined_document):
    """
    returns a tagged text string
    :param timeline:
    :return:
    """
    # TODO: alignment of timestamps to tokens
    timed_tokenlist = timelined_document[1]
    timed_tokens = unicode(''.join([t[1] for t in timed_tokenlist]))
    tagged_text = turktagger.tag_text(timed_tokens)
    tagged_timeline = list()
    for timestamp in timed_tokenlist:

        try:

            tagged_timeline.append({'time':timestamp[0],
                                    'token':timestamp[1],
                                    'pos':tagged_text[timed_tokenlist.index(timestamp)]})
        except IndexError:
            pass
            # print "Index error: " + timestamp

    return {timelined_document[0]: tagged_timeline}


