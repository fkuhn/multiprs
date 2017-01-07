from __future__ import unicode_literals
import yaml


class TrainConfig(object):
    """
    setup for training a parameter file
    """

    def __init__(self, configpath):

        configuration = None
        with open(configpath) as config:
            try:
                configuration = yaml.load(config)

            except yaml.YAMLError as e:
                print e
        germanconf = configuration.get('german')
        self.traintreetagger = configuration.get('traintreetagger')
        self.german_lexicon = configuration.get('lexicon_ger')
        self.german_openclass = configuration.get('openclass_ger')
        self.german_traindata = configuration.get('traindata_ger')


