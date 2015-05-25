#!/usr/bin/env python
import lxml.html as lh
import sys
import re


if len(sys.argv) == 1 :
	print "Please specify bookmark file"
	sys.exit()

bkmark = sys.argv[1];

with open(bkmark,'r') as f : txt = f.read()

doc = lh.fromstring(txt)
results = doc.xpath('//a')
for r in results :
	h = r.get('href')
	if re.search(r'^http',h) : print h
