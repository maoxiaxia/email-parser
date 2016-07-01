#!/bin/bash

# generate the converted txt file from pdf
python main.py

# set up all the input and output files
input="original.txt"
tmp="tmp.txt"
output="final_output.txt"

# remove ^M
tr -d '' < $input > $tmp

input=$tmp

# remove ^L
tr -d '' < $input > $output

# remove the temp file and also the result file
rm $tmp
