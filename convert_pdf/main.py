#!/usr/bin/env python
import pdf_converter

conveted_text = pdf_converter.convert('sample.pdf', pages=None)
print conveted_text
