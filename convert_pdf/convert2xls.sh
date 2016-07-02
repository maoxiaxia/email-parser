#!/bin/bash

# generate the converted txt file from pdf
python pdf2txt.py

tmp="tmp.txt"
output="output.txt"

# iterate through all the converted txt files
TXT_FILES=./txt_files/*txt
for f in $TXT_FILES
do
	input=`echo $f`
	# remove ^M
	tr -d '' < "${input}" > $tmp

	input=$tmp

	# remove ^L
	tr -d '' < "${input}" > $output

	# parse the trimmed outputfile and generate csv file
	python txt2csv.py $output
done

# remove all the txt files and move csv files to csv_file folder
rm *txt
mv *csv csv_files/

# Iterate through each file in the csv files folder
FILES=csv_files/*.csv

for f in $FILES
do
	filename=$(basename "$f")
	
	# Extract the filename without the file extension
	filename="${filename%.*}"
	
	# Convert csv file to xls file with its name
	csv2xls $f -o xls_files/$filename.xls
done
