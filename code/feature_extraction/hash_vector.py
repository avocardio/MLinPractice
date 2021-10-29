#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute the HashingVectorizer for input words.

Created on Wed Sep 29 12:22:13 2021

@author: mkalcher, magmueller, shagemann
"""

from code.feature_extraction.feature_extractor import FeatureExtractor
from sklearn.feature_extraction.text import HashingVectorizer

from code.util import HASH_VECTOR_N_FEATURES


class HashVector(FeatureExtractor):
    """
        Create a Dataframe with shape (number_of_samples, 'HASH_VECTOR_N_FEATURES'). 
        Read the documentation for more information how this works.
    """

    # constructor
    def __init__(self, input_column):
        super().__init__([input_column], "{0}_hashvector".format(input_column))

    def _get_values(self, inputs):
        # inputs is list of text documents
        vectorizer = HashingVectorizer(
            n_features=HASH_VECTOR_N_FEATURES,
            strip_accents="ascii",
            stop_words="english",
            ngram_range=(1, 2),
        )
        # encode document
        vector = vectorizer.fit_transform(inputs[0])
        return vector.toarray()
