#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove all languages that are not equal to input.

* This file was not directly used in the preprocessing, because
we have to remove the entire data rows and not just single 
instances which are not equal to the language input. The language
was thus removed directly in the run_preprocessing.py file.

Created on Wed Sep 22 12:10:13 2021

@author: mkalcher, magmueller, shagemann
"""


from code.preprocessing.preprocessor import Preprocessor
from langdetect import detect
from code.util import COLUMN_TWEET, COLUMN_LANGUAGE


class LanguageRemover(Preprocessor):
    """Remove all non english tweets."""

    # constructor
    def __init__(
        self, input_column=COLUMN_TWEET, output_column=COLUMN_LANGUAGE
    ):  # , language_to_keep = 'en'
        # input column "tweet", new output column
        super().__init__([input_column], output_column)
        # self.language_to_keep = language_to_keep

    # an other approach

    # set internal variables based on input columns
    # def _set_variables(self, inputs):
    # store punctuation for later reference
    # self._punctuation = "[{}]".format(string.punctuation)
    # self.nlp = spacy.load('en')  # 1
    # self.nlp.add_pipe(LanguageDetector(), name='language_detector', last=True) #2

    # get preprocessed column based on data frame and internal variables
    def _get_values(self, inputs):
        column = [detect(tweet) for tweet in inputs[0]]
        return column
