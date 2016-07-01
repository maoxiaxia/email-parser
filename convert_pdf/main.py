#!/usr/bin/env python
import pdf_converter

conveted_text = pdf_converter.convert('format_files/sample.pdf', pages=None)
# print conveted_text

# write the converted result to a file
conveted_text.replace(r'\r', '')
file = open("original.txt", "wb")
file.write(conveted_text)
file.close
