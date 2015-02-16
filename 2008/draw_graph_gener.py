import os,sys

f = os.popen("gnuplot", "w")

f.write("""
#!/usr/bin/gnuplot -persist
#
#    
#    	G N U P L O T
#    	Version 4.2 patchlevel 2 
#    	last modified 31 Aug 2007
#    	System: Linux 2.6.24-19-generic
#    
#    	Copyright (C) 1986 - 1993, 1998, 2004, 2007
#    	Thomas Williams, Colin Kelley and many others
#    
#    	Type `help` to access the on-line reference manual.
#    	The gnuplot FAQ is available from http://www.gnuplot.info/faq/
#    
#    	Send bug reports and suggestions to <http://sourceforge.net/projects/gnuplot>
#    
# set terminal wxt 0
set out \"""" + sys.argv[1] + ".ps\""
"""
set terminal postscript portrait enhanced "Helvetica" 14 
set style arrow 
set grid
set autoscale
set title "2. c) dataset 2" 
set xlabel "Sensitivity"
set ylabel "Specificity"
plot \"""" + sys.argv[1] + ".txt\" with linespoints 1 7 "
)
