#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Radim Rehurek <radimrehurek@seznam.cz>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
Automated tests for checking corpus I/O formats (the corpora package).
"""

from gensim.corpora import bleicorpus, mmcorpus, lowcorpus, svmlightcorpus, \
    dictionary, jsoncorpus
import logging
import os
import os.path
import tempfile
import unittest


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARNING)


module_path = os.path.dirname(__file__) # needed because sample data files are located in the same folder
datapath = lambda fname: os.path.join(module_path, 'test_data', fname)


def testfile():
    # temporary data will be stored to this file
    return os.path.join(tempfile.gettempdir(), 'gensim_corpus.tst')


class CorpusTesterABC(object):
    def __init__(self):
        raise NotImplementedError("cannot instantiate Abstract Base Class")
        self.corpus_class = None # to be overridden with a particular class
        self.file_extension = None # file 'testcorpus.fileExtension' must exist and be in the format of corpusClass


    def test_load(self):
        fname = datapath('testcorpus.' + self.file_extension.lstrip('.'))
        corpus = self.corpus_class(fname)
        docs = list(corpus)
        self.assertEqual(len(docs), 9) # the deerwester corpus always has nine documents, no matter what format


    def test_save(self):
        corpus = [[(1, 1.0)], [], [(0, 0.5), (2, 1.0)], []]

        # make sure the corpus can be saved
        self.corpus_class.save_corpus(testfile(), corpus)

        # and loaded back, resulting in exactly the same corpus
        corpus2 = list(self.corpus_class(testfile()))
        self.assertEqual(corpus, corpus2)

        # delete the temporary file
        os.remove(testfile())

    def test_serialize(self):
        corpus = [[(1, 1.0)], [], [(0, 0.5), (2, 1.0)], []]

        # make sure the corpus can be saved
        self.corpus_class.serialize(testfile(), corpus)

        # and loaded back, resulting in exactly the same corpus
        corpus2 = self.corpus_class(testfile())
        self.assertEqual(corpus, list(corpus2))

        # make sure the indexing corpus[i] works
        for i in xrange(len(corpus)):
            self.assertEqual(corpus[i], corpus2[i])

        # delete the temporary file
        os.remove(testfile())
#endclass CorpusTesterABC


class TestMmCorpus(unittest.TestCase, CorpusTesterABC):
    def setUp(self):
        self.corpus_class = mmcorpus.MmCorpus
        self.file_extension = '.mm'
#endclass TestMmCorpus


class TestSvmLightCorpus(unittest.TestCase, CorpusTesterABC):
    def setUp(self):
        self.corpus_class = svmlightcorpus.SvmLightCorpus
        self.file_extension = '.svmlight'
#endclass TestSvmLightCorpus


class TestBleiCorpus(unittest.TestCase, CorpusTesterABC):
    def setUp(self):
        self.corpus_class = bleicorpus.BleiCorpus
        self.file_extension = '.blei'
#endclass TestBleiCorpus


class TestJsonCorpus(unittest.TestCase):
    def setUp(self):
        pre_path = os.path.join(os.path.dirname(__file__), 'test_data')
        self.cor_path = os.path.join(pre_path, 'very_small.json')


    def test_dict(self):
        """with the small corpus and no filtering, dict length should be 8"""
        corp = jsoncorpus.JsonCorpus(self.cor_path, no_below=0, no_above=1)
        assert len(corp.dictionary) == 8

    def test_filter(self):
        """with the small corpus and standard filtering, length should be 0"""
        corp = jsoncorpus.JsonCorpus(self.cor_path)
        assert len(corp.dictionary) == 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    unittest.main()
