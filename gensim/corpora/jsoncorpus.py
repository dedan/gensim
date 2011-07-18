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


class JsonCorpus(corpora.TextCorpus):

    def __init__(self, input,
                 dictionary=None,
                 no_below=10, no_above=0.5,
                 preprocess=[]):
        """
        Initialize the corpus. This scans the corpus once, to determine its
        vocabulary (only the first `keep_words` most frequent words that
        appear in at least `noBelow` documents are kept).
        """
        self.input = input
        self.preprocess = preprocess
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
            article = json.loads(line)

            s = u""
            for chapter in article[article.keys()[0]].itervalues():
                s = s + u" " + chapter[0]
            length += 1

            s = utils.tokenize(s, lowercase=True)
            for f in self.preprocess:
                s = f(s)
            yield s
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


