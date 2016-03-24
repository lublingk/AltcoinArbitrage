#TODO Figure out cryptsy coin data
#TODO add booleans and error checking
'''
This sheet has preferences and defines the parameters and call functions for every type of exchange.
Currently, it homogenizes the data, but this process may be moved to another file at some point, and the initial calling functions may be restored.
In addition, each exchange may get its own file, again, if I can figure out a good way to automate loading of all exchanges
'''


import urllib,urllib2
import json
import time
import hmac, hashlib
import os
import string

def _createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
  return time.mktime(time.strptime(datestr, format))
  
class exchange:
  PUB_BASE_API_URL = ""
  PRI_BASE_API_URL = ""
  AVAILABLE_METHODS = {}
  
  exchangeData = {}
  lastUpdate = {}
  Constants = {}
  
  APIKey = ""
  Secret = ""
  filename = ""
  #Constructors and Destructors
  def __init__(self, filename=None):
    if(filename == None):
      #stringlower is technically no longer needed
      filename = string.lower(self.__class__.__name__)
    self.loadData(filename)
    self.filename = filename
    Constants = self.exchangeData["__init__"]
    self.APIKey = str(Constants["APIKey"])
    self.Secret = str(Constants["Secret"])
    
  def __del__(self):
    #self.updateData()
    self.saveData(self.filename)
    
  #"Virtual" functions
  def _isSuccess(self, json):
    return True

  def _errorMessage(self, json):
    return ""
  
  def _fetchNewMarketData(self):
    return
    
  def _fetchNewCoinData(self):
    return
  #Base Functions
  
  #Note: this function requires that every inherited class have these methods
  def _fetchNewData(self):
    C = {}
    temp = self._fetchNewMarketData()
    if(temp != None):
      C["Markets"] = temp
    temp = self._fetchNewCoinData()
    if(temp != None):
      C["Coins"] = temp
    C["timestamp"] = time.time()
    return C

  def updateData(self):
    self.lastUpdate = self._fetchNewData()
    self.exchangeData.update(self.lastUpdate)
    return

  #TODO: add option to update just the markets or just the coins
  #def updateCoins(self):
  #def updateMarkets(self):
    
  #this values dynamic data more than static data
  def loadData(self, filename):
    fn = os.path.join(os.path.dirname(__file__), filename)
    stafile = open(fn + "_sta.json","r")
    dynfile = open(fn + "_dyn.json","r")
    self.exchangeData = json.load(stafile)
    self.exchangeData.update(json.load(dynfile))
    stafile.close()
    dynfile.close()
    
  #Update data one last time before saving and closing
  def saveData(self, filename, refetch=False):
    if(refetch==True):
      self.updateData()
    if(self.lastUpdate!={}):
      fn = os.path.join(os.path.dirname(__file__), filename)
      dynfile = open(fn + "_dyn.json","w")
      json.dump(self.lastUpdate, dynfile)
      dynfile.close()
    
  def _post_process(self, before):
    after = before

    # Add timestamps if there isnt one but is a datetime
    if('return' in after):
      if(isinstance(after['return'], list)):
        for x in range(0, len(after['return'])):
          if(isinstance(after['return'][x], dict)):
            if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
              after['return'][x]['timestamp'] = float(_createTimeStamp(after['return'][x]['datetime']))

    return after

  def _unauthenticated_request(self, url):
    url_request_object = urllib2.Request(url)
    response = urllib2.urlopen(url_request_object)
    response_json = {}
    try:
      response_content = response.read()
      response_json = json.loads(response_content)
      return response_json
    finally:
      response.close()
    return "failed"

  def _authenticated_request(self, url, method, post_args={}):
    post_args['method'] = method
    post_args['nonce'] = int(time.time())
    post_data = urllib.urlencode(post_args)
    required_sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
    headers = {}
    headers['key'] = self.APIKey
    headers['sign'] = required_sign
    url_request_object = urllib2.Request(url,
                                       post_data,
                                       headers)
    response = urllib2.urlopen(url_request_object)

    try:
      response_content = response.read()
      response_json = json.loads(response_content)

      if not self._isSuccess(response_json):
        #print response_content
        print "Request failed:", self._errorMessage(response_json)

      return self._post_process(response_json)
    finally:
      response.close()
    return "failed"
  def returnCoins(self):
    return self.exchangeData["Coins"]
  def returnMarkets(self):
    return self.exchangeData["Markets"]
  def returnTimestamp(self):
    return self.exchangeData["timestamp"]