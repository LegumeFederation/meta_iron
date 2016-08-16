#!//usr/bin/env python3
#
#  filesize.py -- returns a dictionary of file attributes.
#
# Example of how to wrap an external command in a way that
# returns values to meta_iron.
#
import sys
if  len(sys.argv) != 2:
   print('Error--filesize requires one file as argument, %d given.'
         %(len(sys.argv)-1))
   sys.exit(1)
print(len(sys.argv))
print('hello')
sys.exit(0)
