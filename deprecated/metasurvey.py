#class definitions for survey data handling
class Survey:
    def __init__(self):
        #must be declared global for access in methods belows.... -.-
        self.entrylist = []
        return

    def addEntry(self, e):
        #e must be a Entry-entity already
        self.entrylist.append(e)
        return

    def getEntries(self):
        for e in self.entrylist:
            print e.data
        return

    def getCorpusKeys(self):
        for ck in self.entrylist:
            #print ck.data
            ck.printCorpusKey()
        return

    def printDataNames(self):
        for ck in self.entrylist:
            print


class Entr: y


def __init__(self, ck=None, data=[]):
    self.corpuskey = ck
    self.data = data
    return


def setCorpusKey(self, ck):
    self.corpuskey = ck
    return


def addData(self, d):
    self.data.append(d)
    return


def printCorpusKey(self):
    print self.corpuskey
    print "."
    return