__author__ = 'kuhn'
import os

from multiprs import corpustools, turkish

PATH = '/home/kuhn/Data/GitHub/multiprs/testdir/'



for i in turkish.pos_tag_directory(PATH):

    print i

