#!/usr/bin/python
"""
Program to plot aligned reads length distribution from a BAM file. Please provide a sorted BAM file.
Usage:
read_length_dist.py <BAM file> 
"""

import pysam 
import re, sys 
from pylab import figure, show
import math
try:
    samfile = pysam.Samfile(sys.argv[1], 'rb')
except:
    print 'Incorrect arguments supplied'
    print __doc__
    sys.exit(-1)
sname=re.search(r'.*\/(\w+)\.bam', sys.argv[1]).group(1)
diff_len=dict()
for alignedread in samfile.fetch():
    if alignedread.qlen in diff_len:
        diff_len[alignedread.qlen]+=1
    else:
        diff_len[alignedread.qlen]=1
samfile.close()
xq, yq = [], []
for length in sorted(diff_len.items()):
    xq.append(length[0])
    yq.append(math.log10(length[1]))
fig = figure()
ax = fig.add_subplot(111)
ax.plot(xq, yq, '-')
ax.set_xlabel('Read length (nts)')
ax.set_ylabel('Nr. of alignments (log-change)')
ax.set_title(sname)
ax.grid(True)
fig.savefig(sname + '.eps', transparent=True)
show()
