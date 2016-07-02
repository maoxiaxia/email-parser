#!/usr/bin/env python
import pdf_converter
import os

path = "./downloads/"
for f in os.listdir(path):
	conveted_text = pdf_converter.convert("%s/%s" % (path, f), pages=None)
	# write the converted result to a file
	file = open("txt_files/%s.txt" % f, "wb")
	file.write(conveted_text)
	file.close
