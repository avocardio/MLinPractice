#!/bin/bash
# overall pipeline for the ML experiments

echo -e "/nloading data"
code/load_data.sh
echo -e "/npreprocessing"
code/preprocessing.sh
echo -e "/nfeature extraction"
code/feature_extraction.sh
#echo "dimensionality reduction"
#code/dimensionality_reduction.sh
echo -e "/nclassification"
code/classification.sh
