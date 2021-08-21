# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 10:05:54 2021

@author: adeni
"""

from boilerpy3 import extractors
import re
import os

pattern = re.compile(r"Q1\/html\/([\w]*)[.html]")
count = 0
directory ="Q1/html/"
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        
        try:
            f =open(os.path.join(directory, filename),"r")
            #where my problem all began
            #reconfigure file encoding to 16
            f.reconfigure(encoding="utf-16")
            text = f.read()
            f.close()
            #Find a match and group in regex compile
            tempName = str(os.path.join(directory, filename))
            m = pattern.match(tempName)
            #change file extension by buildng the string
            textFile_path = "Q1/processed/" + str(m.group(1)) +".txt"

            extractor = extractors.ArticleExtractor()
            content=extractor.get_content(text)
            #print(content)
            p = open(textFile_path,"a")
            p.write(content)
            p.close()
        except Exception as r:
            print(r)       