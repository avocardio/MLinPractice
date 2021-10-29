#!/bin/bash
# overall pipeline for the ML experiments

echo -e "\n loading data"
code/load_data.sh
echo -e "\n preprocessing"
code/preprocessing.sh
echo -e "\n feature extraction"
code/feature_extraction.sh
#echo "dimensionality reduction"
#code/dimensionality_reduction.sh
echo -e "\n classification"
code/classification.sh
