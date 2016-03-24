#!/usr/bin/python

import exchangeTrader

import sys, getopt

def str2bool(str):
  if str.lower() in ("true","yes","t","1"):
    return True
  elif str.lower() in ("false","no","f","0"):
    return False
  else:
    raise TypeError("unsupported argument type")

getNewBool=True
allGoodResultsBool=False
allResultsBool = False

try:
  flagArgs, altArgs = getopt.getopt(sys.argv[1:],"hr:g:a:",["refresh=","allgood=","allresults"])
except getopt.GetoptError:
  print "Invalid Usage: Please try again."
  sys.exit(2)

for flag, parm in flagArgs:
  if flag=="-h":
    print "HELP MENU PLACEHOLDER"
    sys.exit()
  elif flag in ("-r", "--refresh"):
    getNewBool=str2bool(parm)
  elif flag in ("-g", "--allgood"):
    allGoodResultsBool=str2bool(parm)
  elif flag in ("-a", "--allresults"):
    allResultsBool=str2bool(parm)

eT=exchangeTrader.exchangeTrader()
if getNewBool:
  eT.updateAll()

exchFreq=eT.findCommonTrades(2)
#exchFreq=eT.findPaths("coinse","cryptsy")

'''
coinPair="blackcoin-bitcoin"

exchProfit[coinPair]=predictPathProfit(exchanges,exchFreq[coinPair],.05)
for exchPair in exchProfit[coinPair]:
  #if exchProfit[coinPair][exchPair]["profit"]>0:
  print(coinPair,exchPair,exchProfit[coinPair][exchPair]["profit"],exchProfit[coinPair][exchPair]["invested"],str(exchProfit[coinPair][exchPair]["percentprofit"])+"%",exchProfit[coinPair][exchPair]["isAvailable"])
'''
if allGoodResultsBool:
  print "Pair, Direction, Profit, Invested, PercentProfit, IsAvailable"
else:
  print "Pair, Direction, Profit, Invested, PercentProfit"
#NOTE: .05 is used for both LTC and BTC here. Make sure to keep track of that"
exchProfit=eT.predictAllPathsProfit(exchFreq,.05)
for coinPair in exchProfit:
  for exchPair in exchProfit[coinPair]:
    if allResultsBool:
      print str(coinPair),str(exchPair),exchProfit[coinPair][exchPair]["profit"],exchProfit[coinPair][exchPair]["invested"],str(exchProfit[coinPair][exchPair]["percentprofit"])+"%",exchProfit[coinPair][exchPair]["isAvailable"]
    elif allGoodResultsBool:
      if exchProfit[coinPair][exchPair]["profit"]>0:
        print str(coinPair),str(exchPair),exchProfit[coinPair][exchPair]["profit"],exchProfit[coinPair][exchPair]["invested"],str(exchProfit[coinPair][exchPair]["percentprofit"])+"%",exchProfit[coinPair][exchPair]["isAvailable"]
    else:
      if exchProfit[coinPair][exchPair]["percentprofit"]>3 and exchProfit[coinPair][exchPair]["isAvailable"]:
        print str(coinPair),str(exchPair),exchProfit[coinPair][exchPair]["profit"],exchProfit[coinPair][exchPair]["invested"],str(exchProfit[coinPair][exchPair]["percentprofit"])+"%"


    
#file=open("dumpfile2.txt","w")
#json.dump(exchFreq,file)