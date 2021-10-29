#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute the word2vec for each tokenized word.

Created on Wed Sep 29 12:22:13 2021

@author: mkalcher, magmueller, shagemann
"""

import numpy as np
import gensim.downloader as api
import ast
from code.feature_extraction.feature_extractor import FeatureExtractor

class Word2Vec(FeatureExtractor):
    """
        Create Word2Vec feature.
        Read sklearn or our documentation for more information.
    """

    # constructor
    def __init__(self, input_column):
        super().__init__([input_column], "tweet_word2vec")

    # don't need to fit, so don't overwrite _set_variables()

    def _get_values(self, inputs):

        embeddings = api.load(
            "word2vec-google-news-300"
        )  # Alternative: glove-twitter-200 for classifier
        keywords = [
            "coding",
            "free",
            "algorithms",
            "statistics",
        ]  # deeplearning not present

        tokens = inputs[0].apply(
            lambda x: list(ast.literal_eval(x))
        )  # Column from Series to list

        similarities = []

        for rows in tokens:
            sim = []
            for word in keywords:
                for item in rows:
                    try:
                        sim.append(embeddings.similarity(item, word))
                    except KeyError:
                        pass
            # similarities.append(max(sim)-np.std(sim))
            similarities.append(round(np.mean(sim), 4))  # try median

        result = np.asarray(similarities)
        result = result.reshape(-1, 1)
        return result
