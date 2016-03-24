#!/usr/bin/python

import json

file = open("cryptsy_dyn.json","r")
comb=json.load(file)
file.close()
A=[]
for key in comb["Markets"]:
  A.append(comb["Markets"][key]["start"])

A=list(set(A))
A.sort()
gile = open("cryptsycointemp.txt","w")
json.dump(A,gile)