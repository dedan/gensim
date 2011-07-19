#!/usr/bin/env python
# encoding: utf-8
"""
textfilescorpus.py

This is a simple textcorpus which can be used when the documents of a corpus
are spread over one file each.

Created by Stephan Gabler on 2011-06-27.
"""

from gensim import corpora, utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.mmcorpus import MmCorpus
from os import path
import glob
import logging
import string

logger = logging.getLogger('gensim.corpora.jsoncorpus')

def getstream(input):
    """
    input is the path to the folder where the separate textfiles reside
    """
    assert input is not None
    assert isinstance(input, basestring)
    flist = glob.glob(path.join(input, '*.txt'))
    if not flist:
        raise ValueError('no textfiles found')
    for file in flist:
        with open(file) as f:
            yield string.join(f.readlines())


class TextFilesCorpus(corpora.TextCorpus):

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
            length += 1
            s = utils.tokenize(line, lowercase=True)
            for f in self.preprocess:
                s = f(s)
            yield s
        self.length = length


    def getstream(self):
        return getstream(self.input)


    def __len__(self):
        """Define this so we can use `len(corpus)`"""
        if 'length' not in self.__dict__:
            logging.info("caching corpus size (calculating number of documents)")
            self.length = sum(1 for doc in self.get_texts())
        return self.length


