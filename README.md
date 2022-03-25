Email-Parser
============
[![Build Status](https://travis-ci.org/luo149/gmail-parser.svg?branch=master)](https://travis-ci.org/luo149/gmail-parser)

It's a basic email parser which aims at sorting out the attachment files from given contacts. It mainly focuses on getting statistics related attachments. After getting targeted attachments, it parses the attachments of different formats to one uniform format. Here I choose csv, which is the most plain text format, as the uniform format. This indeed would save much time for those who have to repeatedly click mouse and do number of copy and paste to get this task done.

Usually, the attachment comes in format of excel, pdf, csv(this would be nice because this is the format I want to convert to).

So far, it focuses on converting pdf attachment since excel and csv are not a concern.
