'''
This module runs back end calcalutions and evaluates the best arbitrage opportunity
First step would probably be to check time stamp of retrieved data and then check if it is still usuable.
'''
import os, importlib, json, itertools

class exchangeTrader:
  Coins = {}
  Markets = {}
  exchangeNames = []
  def __init__(self):
    self.Exchanges = {}
    self.exchanges = {}
    #this import process can be greatly improved, but works for now
    for fn in os.listdir('./lib'):
      if(os.path.isfile("./lib/"+fn) and (fn[0] != "_") and (fn[-3:] == ".py")):
        exchangeName=fn[:-3]
        self.Exchanges[exchangeName]=(importlib.import_module("lib."+exchangeName))
        self.exchanges[exchangeName]=getattr(self.Exchanges[exchangeName], exchangeName)()
        self.Coins[exchangeName] = self.exchanges[exchangeName].returnCoins()
        self.Markets[exchangeName] = self.exchanges[exchangeName].returnMarkets()
        self.exchangeNames.append(exchangeName)

  #add error checking
  def updateAll(self):
    for i in self.exchanges:
      self.exchanges[i].updateData()
      self.Coins[i] = self.exchanges[i].returnCoins()
      self.Markets[i] = self.exchanges[i].returnMarkets()
    return True
    
  #def updateMarkets(self):
  
  #def updateCoins(self):
  
  #def updateExchange(self,exchange):
    
  '''
  Below Are the problems I need to fix here
  1. Quark and Quarkcoin between cryptsy and coinse are the same thing. This means that quark wrongly wont be considered for arbitrage
  '''
  #May want to use this function to check if a new coin has been added.
  def getAllCoinTypes(self):
    X=[]
    for j in self.Coins:
      X.append(str(j))
    X=list(set(X))
    X.sort()
    return X

  #This function finds all common trade between all exchanges. Recommended to use both directions mode for arbitrageprofit function
  def findCommonTrades(self,minFreq=2):
    exchangeFreq={}
    for i in self.Markets:
      for j in self.Markets[i]:
        if j in exchangeFreq:
          exchangeFreq[j]["exchanges"].append(i)
        else:
          exchangeFreq[j]={}
          exchangeFreq[j]["start"]=self.Markets[i][j]["start"]
          exchangeFreq[j]["end"]=self.Markets[i][j]["end"]
          exchangeFreq[j]["exchanges"]=[]
          exchangeFreq[j]["exchanges"].append(i)
    for k,v in exchangeFreq.items():
      if(len(v["exchanges"])<minFreq):
        del exchangeFreq[k]
    return exchangeFreq
  
  #This function finds all routes from a given starting to another, excluding a straight withdrawal. It's return format is identical to the findCommonTrades function above.
  def findPaths(self, startMarket, endMarket=None):
    exchangeFreq={}
    filterEndBool = (endMarket is not None)
    for I in self.Markets[startMarket]:
      exchangeFreq[I]={}
      exchangeFreq[I]["start"]=self.Markets[startMarket][I]["start"]
      exchangeFreq[I]["end"]=self.Markets[startMarket][I]["end"]
      exchangeFreq[I]["exchanges"]=[]
      exchangeFreq[I]["exchanges"].append(startMarket)
    for i in self.Markets:
      for j in self.Markets[i]:
        if (j in exchangeFreq) and (i != startMarket):
          if not filterEndBool:
            exchangeFreq[j]["exchanges"].append(i)
          elif i == endMarket:
            exchangeFreq[j]["exchanges"].append(i)
    for k,v in exchangeFreq.items():
      if(len(v["exchanges"])<2):
        del exchangeFreq[k]
    return exchangeFreq

  #TODO: write function that gets all market and coin data or just specific and use here and in other places
  #TODO: Add confirmation time and market volatility parameters to coins(money transfer time shouldn't take longer than projected opportunity period.
  #TODO: Eventually look into using another type of coin with a faster confirmation speed as a carrier
  #TODO: Add more market depth to consideration to figure out TOTAL possible profit.
  #TODO: Dynamically get cryptsy withdrawal fees(there is a way). Will probably need to write custom update function to join with statics
  #TODO: Add slow update fetches coindata(so now three types: Fast(exchanges), slow(coins), and Static(not updated)
  #TODO: do min of intermediate result and possible back thingy....(work backwards to find investable amount)
  #TODO: revise while thinking about eveything as a one waypath and using current balances
  #This function currently calculates the profit from this two step process:
  #1: Buy a currency using either BTC or LTC on any exchange and then withdraw it.
  #2: Sell the currency on any other exchange and withdraw the resulting BTC/LTC back to the original exhcnage.
  #In the future it will be revised to consider one step at a time and consider another method of currency return besides direct withdrawal.
  def predictPathProfit(self,exchangeFreqEntry,investableAmount,bothDirections=True):
    result = {}
    try:
      if bothDirections:
        Perms=itertools.permutations(exchangeFreqEntry["exchanges"],2)
      else:
        Perms=itertools.combinations(exchangeFreqEntry["exchanges"],2)
      for startMarket, endMarket in Perms:
        startCoin=exchangeFreqEntry["end"]
        endCoin=exchangeFreqEntry["start"]
        
        isAvailable = self.Coins[startMarket][startCoin]["useable"] and self.Coins[startMarket][endCoin]["useable"] and self.Coins[endMarket][startCoin]["useable"] and self.Coins[endMarket][endCoin]["useable"] and self.Markets[startMarket][endCoin+"-"+startCoin]["useable"] and self.Markets[endMarket][endCoin+"-"+startCoin]["useable"]
        
        startRate=float(self.Markets[startMarket][endCoin+"-"+startCoin]["bestsell"]["price"])
        startQuantity=float(self.Markets[startMarket][endCoin+"-"+startCoin]["bestsell"]["quantity"])
        startTradeFeePercent=float(self.Coins[startMarket][endCoin]["buy_trade_fee_percent"])
        startWithdrawalFee=float(self.Coins[startMarket][endCoin]["withdrawal_fee"])
        
        endRate=float(self.Markets[endMarket][endCoin+"-"+startCoin]["bestbuy"]["price"])
        endQuantity=float(self.Markets[endMarket][endCoin+"-"+startCoin]["bestbuy"]["quantity"])
        endTradeFeePercent=float(self.Coins[endMarket][startCoin]["sell_trade_fee_percent"])
        endWithdrawalFee=float(self.Coins[endMarket][startCoin]["withdrawal_fee"])
        
        investedAmount=min(startRate*startQuantity,(((endRate*endQuantity)+startWithdrawalFee*startRate)/(1-(startTradeFeePercent/100))),investableAmount)
        try:
          intermediateAmount=(investedAmount/startRate)*(1-(startTradeFeePercent/100))-startWithdrawalFee
          isNotErrored=True
        except ZeroDivisionError:
          intermediateAmount=0
          investedAmount=0
          isNotErrored=False
        
        endAmount=(intermediateAmount*endRate)*(1-(endTradeFeePercent/100))#-endWithdrawalFee
        
        profit=endAmount-investedAmount
        
        
        result[startMarket+"->"+endMarket]={}
        result[startMarket+"->"+endMarket]["profit"]=profit
        result[startMarket+"->"+endMarket]["invested"]=investedAmount
        try:
          result[startMarket+"->"+endMarket]["percentprofit"]=(profit/investedAmount)*100
        except ZeroDivisionError:
          result[startMarket+"->"+endMarket]["percentprofit"]=-101
          
        result[startMarket+"->"+endMarket]["isAvailable"]=(isAvailable and isNotErrored)
    except KeyError:
      pass
    
    return result

  #This one does not sort
  #TODO: make outer array be exchange pair, not coin pair.
  def predictAllPathsProfit(self,exchangeFreq,investableAmount,bothDirections=True):
    result = {}
    for I in exchangeFreq:
      A=self.predictPathProfit(exchangeFreq[I],investableAmount, bothDirections)
      result[I]=A
    return result

  #This one sorts-ish, but butchers indices, horribly
  #TODO: make outer array be exchange pair, not coin pair.
  def predictAllPathsProfitAlt(self,exchangeFreq,investableAmount,bothDirections=True):
    result = {}
    for I in exchangeFreq:
      A=self.predictPathProfit(exchangeFreq[I],investableAmount, bothDirections)
      for J in A:
        result[str(I)+" "+str(J)]=A[J]
    result=sorted(result.items(), key=lambda (k,v): v["percentprofit"], reverse=True)
    return result
    