#!/bin/bash

# generate the converted txt file from pdf
python pdf2txt.py

# set up all the input and output files
input="original.txt"
tmp="tmp.txt"
output="final_output.txt"

# remove ^M
tr -d '' < $input > $tmp

input=$tmp

# remove ^L
tr -d '' < $input > $output

# replace \t with space

# remove the temp file and also the result file
rm $tmp

# parse the trimmed outputfile and generate the csv file
python generate_csv.py $output

# remove all the txt files and move csv files to output_file folder
rm *txt
mv *csv csv_files/

# convert generated output file to xls

# Iterate through each file in the csv files folder
FILES=csv_files/*.csv

for f in $FILES
do
	echo "file $f"
	cat $f
done

csv2xls csv_files/*csv -o xls_files/out.xls
