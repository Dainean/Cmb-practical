#!/usr/bin/env python
#op11question7.py
#Write an Ascii file with your text editor with 10 rows and two columns with arbitrary numbers.
#data file is called onzindata.dat
#Write a program that reads this data in two arrays 'x' and 'y'. Print for both arrays the minimum and #maximum value and the mean (use array methods or array attributes, no for loops).
#Calculate a new array: y2 = (y - y_mean)**2 and print its contents. 

from kapteyn import tabarray
import numpy as np

x, y = tabarray.readColumns('onzindata.dat' ,'#, cols=(0,1) )

print x
