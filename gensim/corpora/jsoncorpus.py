#!/usr/bin/env python
# encoding: utf-8
"""
jsoncorpus.py

Created by Stephan Gabler on 2011-06-27.
"""

from gensim import corpora, utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.mmcorpus import MmCorpus
from gensim.parsing.preprocessing import preprocess_string
import json
import logging
import sys
import traceback

logger = logging.getLogger('gensim.corpora.jsoncorpus')
#dictionary.filterExtremes(noBelow=2) # post-process the dictionary: remove tokens that are too frequent or too infrequent
#14:46:35 Jose Quesada: before (in the mar2008 english parsing) we used <10
#14:46:45 Stephan Gabler: ok
#14:46:55 Jose Quesada: for too frequent, we can use a stoplist
#14:47:05 Jose Quesada: there should be many for german floating around
#14:47:25 Stephan Gabler: ok
#14:47:46 Jose Quesada: but you can tell gensim to drop anything above fq=10000 or somesuch

class JsonCorpus(corpora.TextCorpus):

    def __init__(self, input, dictionary=None, no_below=10, no_above=0.5):
        """
        Initialize the corpus. This scans the corpus once, to determine its
        vocabulary (only the first `keep_words` most frequent words that
        appear in at least `noBelow` documents are kept).
        """
        self.input = input
        if dictionary:
            self.dictionary = dictionary
        else:
            self.dictionary = Dictionary()
            if input is not None:
                self.dictionary.add_documents(self.get_texts())
                self.dictionary.filter_extremes(no_below=no_below, no_above=no_above)
            else:
                logger.warning("No input document stream provided !!!")


    def get_texts(self):
        """
        Parse documents from the .cor file provided in the constructor. Lowercase
        each document and ignore some stopwords.

        .cor format: one document per line, words separated by whitespace.
        """
        length = 0
        for line in self.getstream():
            if length < 999000:
                continue
            try:
                article = json.loads(line)
            except Exception as inst:
                print line
                print inst
                for tb in traceback.format_tb(sys.exc_info()[2]):
                    print tb

            s = u""
            for chapter in article[article.keys()[0]].itervalues():
                s = s + u" " + chapter[0]
                print chapter[0]
            print s
            length += 1
            if (length % 1000) == 0:
                print length

            yield utils.tokenize(s, lowercase=True)
        self.length = length

    def __len__(self):
        """Define this so we can use `len(corpus)`"""
        if 'length' not in self.__dict__:
            logging.info("caching corpus size (calculating number of documents)")
            self.length = sum(1 for doc in self.get_texts())
        return self.length

if __name__ == '__main__':
    print 'start'
    bla = JsonCorpus("/data/corpora/wiki/wiki_de_2011/wiki.json")
    print bla.dictionary
    for line in bla.get_texts():
        print list(line)
    MmCorpus.serialize('/data/corpora/wiki/wiki_de_2011/de_bow.mm', bla, progress_cnt=10000)


