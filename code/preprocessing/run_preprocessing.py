#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runs the specified collection of preprocessing steps

Created on Tue Sep 28 16:43:18 2021

@author: lbechberger
"""

import argparse, csv, pickle
import pandas as pd
from tqdm import tqdm
from sklearn.pipeline import make_pipeline
from code.preprocessing.punctuation_remover import PunctuationRemover
from code.preprocessing.string_remover import StringRemover
from code.preprocessing.tokenizer import Tokenizer
from code.util import COLUMN_TWEET, SUFFIX_TOKENIZED, COLUMN_LANGUAGE, COLUMN_PREPROCESS

# setting up CLI
parser = argparse.ArgumentParser(description="Various preprocessing steps")
parser.add_argument("input_file", help="path to the input csv file")
parser.add_argument("output_file", help="path to the output csv file")
parser.add_argument(
    "-p",
    "--punctuation",
    action="store_true",
    help="remove punctuation and special characters",
)
parser.add_argument(
    "-s", "--strings", action="store_true", help="remove stopwords, links and emojis"
)
parser.add_argument(
    "-t",
    "--tokenize",
    action="store_true",
    help="tokenize given column into individual words",
)
# parser.add_argument("--tokenize_input", help = "input column to tokenize", default = 'output')
parser.add_argument(
    "-e",
    "--export_file",
    help="create a pipeline and export to the given location",
    default=None,
)
parser.add_argument(
    "--language", help="just use tweets with this language ", default=None
)

args = parser.parse_args()

# load data
df = pd.read_csv(
    args.input_file, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n", low_memory=False
)


# collect all preprocessors
preprocessors = []
if args.punctuation:
    preprocessors.append(PunctuationRemover(COLUMN_TWEET, COLUMN_PREPROCESS))
if args.strings:
    preprocessors.append(StringRemover(COLUMN_PREPROCESS, COLUMN_PREPROCESS))
if args.tokenize:
    preprocessors.append(
        Tokenizer(COLUMN_PREPROCESS, COLUMN_PREPROCESS + SUFFIX_TOKENIZED)
    )


len_before = df[COLUMN_TWEET].str.len().sum()


# This is the part we used instead if the language_remover.py file
if args.language is not None:
    # filter out one language
    before = len(df)
    df = df[df["language"] == args.language]
    after = len(df)
    print("Filtered out: {0} (not 'en')".format(before - after))
    df.reset_index(drop=True, inplace=True)

# call all preprocessing steps
for preprocessor in tqdm(preprocessors):
    df = preprocessor.fit_transform(df)

len_after = df[COLUMN_PREPROCESS].str.len().sum()
print("/nNumber of chars before preprocessing: {}".format(len_before))
print("Number of chars after preprocessing: {}".format(len_after))
print(
    "Removed: {0} ({1}%)".format(
        len_before - len_after, (len_before - len_after) * 100 / len_before
    )
)

# drop useless line which makes problems with csv
del df["trans_dest\r"]
# store the results
df.to_csv(
    args.output_file, index=False, quoting=csv.QUOTE_NONNUMERIC, line_terminator="\n"
)

# create a pipeline if necessary and store it as pickle file
if args.export_file is not None:
    pipeline = make_pipeline(*preprocessors)
    with open(args.export_file, "wb") as f_out:
        pickle.dump(pipeline, f_out)

