#!/usr/bin/env python3
import sys
import os
import tempfile

tmp=tempfile.mkstemp()

with open(sys.argv[1]) as fd1, open(tmp[1],'w') as fd2:
    for line in fd1:
        line = line.replace('blue','azure')
        fd2.write(line)

os.rename(tmp[1],sys.argv[1])
