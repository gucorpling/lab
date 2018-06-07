#!/usr/bin/python
# -*- coding: utf-8 -*-

print("Content-type:text/html\r\n\r\n")

import io, sys, re, os, cgi
from glob import glob
from collections import OrderedDict
from six import iteritems, iterkeys

files = glob("updates/*.html")

posts_template = """								
									<div class="mini-posts">
									**posts**
									</div>
"""

posts = {}

for infile in files:
	if "template" not in infile and "index" not in infile:
		text = io.open(infile,encoding="utf8").read()
		filename = os.path.basename(infile)

		m = re.search(r'(<article.*?</article>)',text,re.MULTILINE|re.DOTALL)
		if m is None:
			continue
		else:
			article = m.group(1).replace("<br>","").replace("<br/>","")

		m = re.search(r'datetime="(20[0-9][0-9]-[01][0-9]-[0-3][0-9])"',text,re.MULTILINE|re.DOTALL)
		if m is None:
			continue
		else:
			date = m.group(1)

		# Pretty indent
		article = article.replace("<","\t"*10+"<")
		article = article.replace("\t<a ","\t\t<a ")
		article = article.replace("\t<p","\t\t<p")
		posts[date] = article

posts = OrderedDict(sorted(iteritems(posts),reverse=True))

post_limit = cgi.FieldStorage().getvalue("posts",None)

if post_limit == "all":
	limit = 10000
else:
	limit = 4

limit = min(limit,len(posts))
output = ""

for i, p in enumerate(iterkeys(posts)):
	date = p
	post = posts[p]
	if i > limit -1:
		if 'sticky="true"' not in post.lower():
			continue
	if post_limit == "all":
		post = post.replace('"images/','"../images/')  # Handle image src if specified relative to corpling/
		post = re.sub(r'(<article[^>]+>)',r'\1' + 10*"\t" + '<p><b>' + date + '</b></p>\n',post)
	output += post

output = posts_template.replace("**posts**",output)

print(output.encode("utf8"))
