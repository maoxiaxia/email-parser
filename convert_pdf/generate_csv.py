#!/usr/bin/python
import os
import sys
import tempfile


def main():
    # Open file
    file_name = sys.argv[1]
    fp = open(file_name, "r")
    
    # Close the file
    fp.close()

if __name__ = '__main__':
    main()
