#!/usr/bin/python

import exchangeTrader,json

import sys, getopt

def str2bool(str):
  if str.lower() in ("true","yes","t","1"):
    return True
  elif str.lower() in ("false","no","f","0"):
    return False
  else:
    raise TypeError("unsupported argument type")

getNewBool=True
maxPrint=5
allResultsBool = False

try:
  flagArgs, altArgs = getopt.getopt(sys.argv[1:],"hr:n:a:",["refresh=","numargs=","allresults"])
except getopt.GetoptError:
  print "Invalid Usage: Please try again."
  sys.exit(2)

for flag, parm in flagArgs:
  if flag=="-h":
    print "HELP MENU PLACEHOLDER"
    sys.exit()
  elif flag in ("-r", "--refresh"):
    getNewBool=str2bool(parm)
  elif flag in ("-n", "--numargs"):
    maxPrint=int(parm)
  elif flag in ("-a", "--allresults"):
    allResultsBool=str2bool(parm)

eT=exchangeTrader.exchangeTrader()
if getNewBool:
  eT.updateAll()

A=eT.findPaths("coinse","cryptsy")
result = eT.predictAllPathsProfitAlt(A,0.05,False)
print "Forward"
print "Pair, Direction, Profit, Invested, PercentProfit"

printIndex=0
for index,value in result:
  if (not allResultsBool) and (printIndex == maxPrint):
    break
  if value["isAvailable"]:
    print index, value["profit"],value["invested"],str(value["percentprofit"])+"%"
    printIndex=printIndex+1
A=eT.findPaths("cryptsy","coinse")
result = eT.predictAllPathsProfitAlt(A,0.05,False)

print "Backward"
print "Pair, Direction, Profit, Invested, PercentProfit"
printIndex=0
for index,value in result:
  if (not allResultsBool) and (printIndex == maxPrint):
    break
  if value["isAvailable"]:
    print index, value["profit"],value["invested"],str(value["percentprofit"])+"%"
    printIndex=printIndex+1