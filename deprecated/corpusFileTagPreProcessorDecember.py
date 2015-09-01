__author__ = 'fkuhn'

#this script checks whether the corpus training files contain valid tags or not.

import re


class ValidTags:
    """
    A Class for valid pos-tags of a certain language.
    """

    def __init__(self, tagfilename, remarks):
        assert isinstance(tagfilename, basestring)
        #read in lines and delete the linefeed character
        self.tags = open(tagfilename).read().rsplit('\n')
        #a list of valid remark-suffixes
        self.remark_suffixes = remarks

    def is_valid_tag(self, tagstring):
        """
        checks if given tagstring is in valid tag list.
        if a person number digit is found, it is also marked True

        @param tagstring: a tag to be evaluated
        @type tagstring: basetring
        @return boolean
        """
        #play it safe: convert tagstring to majuscel
        tagstring = tagstring.strip()
        tagstring = tagstring.upper()

        #first check if there is a person number digit suffix
        if re.match('[A-Z]+[0-9]?', tagstring) is not None:
            tagmatch = re.match('([A-Z]+)[0-9]?', tagstring)
            tagstringmatch = tagmatch.group(1)
            #if yes, check if the tag without the number suffix is in list

            if tagstringmatch in self.tags:
                return True

        return False

    def is_valid_postag(self, tagstring):
        """
        just checks if a string is a single postag and valid
        @param tagstring:
        @return:
        """
        try:
            tagmatch = re.match('([A-Z]+)([1-3]?)([A-Z]*)', tagstring)
            prefix = tagmatch.group(1)
            number = tagmatch.group(2)
            suffix = tagmatch.group(3)
        except:
            return False
        for valid_tag in self.tags:
            if prefix == valid_tag and suffix != "":
                if suffix in self.tags:
                    return True
                if suffix in self.remark_suffixes:
                    return True
            if prefix == valid_tag:
                return True
        return False

    def del_remarks(self, tagstring):
        """
        deletes valid remark suffixes. returns tagstring
        """
        t = tagstring
        tagmatch = re.match('([A-Z]+)([1-3]?)([A-Z]*)', t)
        if tagmatch.group(3):
            t = tagmatch.group(1) + tagmatch.group(2)
        return t


    def is_valid_postag_composite(self, tagstring):
        """
        check if postag is a composite
        @param tagstring:
        @return:
        """
        composite = self.postag_composite(tagstring)
        if composite > 1:
            return True
        return False

    def postag_composite(self, tagstring, composite_count=0):
        """
        This methods checks if a tagstring is composed of 2 or more valid postags.
        if this is true, it is regarded as a valid tag as well.
        note-suffixes must be omitted
        @param tagstring:
        @return:
        """
        #TODO: not yet working
        tagstring_backup = tagstring
        #iterate over reverse string
        for item in tagstring:
            if len(tagstring) > 1:

                if self.is_valid_postag(tagstring):
                    print tagstring
                    composite_count += 1
                    #if valid substring is found. recursevily invoke this method with the rest of the string
                    composite_count = self.postag_composite(tagstring_backup.strip(tagstring), composite_count)
                tagstring = tagstring.strip(tagstring[-1])
        return composite_count

    def get_nearest_tag(self, tagstring):
        """
        searches for the most similar tag in the valid tag list
        @type tagstring: basestring
        """

        #remove trailing whitespace
        tagstring = tagstring.strip()
        #play it safe: convert tagstring to majuscel
        tagstring = tagstring.upper()

        #check if tag is in valid list
        #if self.is_valid_tag(tagstring) is True:
        #    return tagstring

        #first, get all distance scores for the given tagstring.
        distscore_triples = []
        #notation: (tagstring, validstring, distance)
        tagnumber = ''
        #if tagstring of unknown tag has a number delimeter. remove it

        if re.match('[A-Z]+[0-9]+[A-Z]+', tagstring) is not None:
            tagmatch = re.match('([A-Z]+)([0-9]+)([A-Z]+)', tagstring)
            #create a new tagstring: omit the number matched in group 2
            tagstring = tagmatch.group(1) + tagmatch.group(3)
            tagnumber = tagmatch.group(2)
        if re.match('[A-Z]+[0-9]+', tagstring) is not None:
            tagmatch = re.match('([A-Z]+)([0-9]+)', tagstring)
            tagstring = tagmatch.group(1)
            tagnumber = tagmatch.group(2)
        #check if tagstring is agglutinated
        else:
            return None

        for tagitem in self.tags:
            distscore_triples.append((tagstring, tagitem, self.dameraulevenshtein(tagstring, tagitem)))
            #get minimal distance tag
        neartag_triple = ('x', 'y', 99)  # a dummy triple
        for item in distscore_triples:
            if neartag_triple[2] > item[2]:
                neartag_triple = item
        return neartag_triple[1] + tagnumber

    @staticmethod
    def dameraulevenshtein(seq1, seq2):

        """
        Calculate the Damerau-Levenshtein distance between sequences.
            This distance is the number of additions, deletions, substitutions,
            and transpositions needed to transform the first sequence into the
            second. Although generally used with strings, any sequences of
            comparable objects will work.

            Transpositions are exchanges of *consecutive* characters; all other
            operations are self-explanatory.

            This implementation is O(N*M) time and O(M) space, for N and M the
            lengths of the two sequences.

            #>>> dameraulevenshtein('ba', 'abc')
            2
            #>>> dameraulevenshtein('fee', 'deed')
            2

            It works with arbitrary sequences too:
            #>>> dameraulevenshtein('abcd', ['b', 'a', 'c', 'd', 'e'])
            2
        """
        # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
        # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1 matrix.
        # However, only the current and two previous rows are needed at once,
        # so we only store those.
        oneago = None
        thisrow = range(1, len(seq2) + 1) + [0]
        for x in xrange(len(seq1)):
            # Python lists wrap around for negative indices, so put the
            # leftmost column at the *end* of the list. This matches with
            # the zero-indexed strings and saves extra calculation.
            twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
            for y in xrange(len(seq2)):
                delcost = oneago[y] + 1
                addcost = thisrow[y - 1] + 1
                subcost = oneago[y - 1] + (seq1[x] != seq2[y])
                thisrow[y] = min(delcost, addcost, subcost)
                # This block deals with transpositions
                if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                    and seq1[x - 1] == seq2[y] and seq1[x] != seq2[y]):
                    thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
        return thisrow[len(seq2) - 1]





