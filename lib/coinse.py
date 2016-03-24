import string
import _exchange

class coinse(_exchange.exchange):
  PUB_BASE_API_URL = "https://www.coins-e.com/api/v2/"
  PRI_BASE_API_URL = "https://www.coins-e.com/api/v2/"
  '''
  AVAILABLE_METHODS = {
                      "public": {"placeholder"},
                      "private": {"placeholder"}
                      }
  '''
  def _isSuccess(self, json):
    return json['status'] == "true"

  def _errorMessage(self, json):
    return json['message']

  #TODO edit function and make functions below use it
  '''
  def api_query(self, method, req={}):
    if(method == "marketdata" or method == "orderdata" or method == "marketdatav2"):
      return self._unauthenticated_request(self.PUB_BASE_API_URL + method)
    elif(method == "singlemarketdata" or method == "singleorderdata"):
      return self._unauthenticated_request(self.PUB_BASE_API_URL + method + '&marketid=' + str(req['marketid']))
    else:
      return self._authenticated_request(self.PRI_BASE_API_URL, method, req)
  '''

  #TODO: Double check buy and sell values and switch if needed
  #TODO: Account for multiple ongoing trades(aka. don't use best numbers if trading same thing)
  #TODO: Figure out what max tradeable profitable volume is.
  #TODO: ADD More market depth to all exchanges
  def _fetchNewMarketData(self):
    C = {}
    A = self._getMarkets()
    B = self._getConsolData()
    for x in range(0, len(A["markets"])):
      name = A["markets"][x]["pair"]
      startname = string.lower(A["markets"][x]["coin1"])
      endname = string.lower(A["markets"][x]["coin2"])
      combname = startname + "-" + endname
      C[combname] = {
        "name": name,
        "start": startname,
        "end": endname,
        "marketid": name,
        "useable": (B["markets"][name]["status"] == "healthy")
      }
      try:
        C[combname]["bestsell"] = {
          "price": B["markets"][name]["marketstat"]["ask"],
          "quantity": B["markets"][name]["marketstat"]["ask_q"]
          }
      except TypeError:
        C[combname]["bestsell"] = {
          "price": None,
          "quantity": None
          }
      try:
        C[combname]["bestbuy"] = {
          "price": B["markets"][name]["marketstat"]["bid"],
          "quantity": B["markets"][name]["marketstat"]["bid_q"]
          }
      except TypeError:
        C[combname]["bestbuy"] = {
          "price": None,
          "quantity": None
          }
    return C
  '''
  #Old array based method
  def _fetchNewMarketData(self):
    C = []
    A = self._getMarkets()
    B = self._getConsolData()
    for x in range(0, len(A["markets"])):
      name = A["markets"][x]["pair"]
      C.append({
        "name": name,
        "start": string.lower(A["markets"][x]["coin1"]),
        "end": string.lower(A["markets"][x]["coin2"]),
        "marketid": name,
        "bestsell": {
          "price": B["markets"][name]["marketstat"]["ask"],
          "quantity": B["markets"][name]["marketstat"]["ask_q"]
        },
        "bestbuy": {
          "price": B["markets"][name]["marketstat"]["bid"],
          "quantity": B["markets"][name]["marketstat"]["bid_q"]
        }
      })
    return C
  '''

  #TODO: ADD More elements(confirmation time, Address, balance)
  #TODO: Filter out USD, mining contracts, etc.
  #TODO: homogenize quark/quarkcoin
  def _fetchNewCoinData(self):
    C = {}
    A = self._getCoins()
    for x in range(0, len(A["coins"])):
      name=string.lower(A["coins"][x]["name"])
      C[name]={
        "buy_trade_fee_percent": A["coins"][x]["trade_fee_percent"],
        "sell_trade_fee_percent": A["coins"][x]["trade_fee_percent"],
        #"trade_fee": A["coins"][x]["trade_fee"],
        "withdrawal_fee": A["coins"][x]["withdrawal_fee"],
        "coinid": A["coins"][x]["coin"],
        "useable": (A["coins"][x]["status"] == "healthy")
      }
    return C
  '''
  #Old Array Based Method
  def _fetchNewCoinData(self):
    C = []
    A = self._getCoins()
    for x in range(0, len(A["coins"])):
      C.append({
        "name": string.lower(A["coins"][x]["name"]),
        "trade_fee_percent": A["coins"][x]["trade_fee_percent"],
        #"trade_fee": A["coins"][x]["trade_fee"],
        "withdrawal_fee": A["coins"][x]["withdrawal_fee"],
        "coinid": A["coins"][x]["coin"]
      })
    return C
  '''

  def _getMarkets(self):
    return self._unauthenticated_request(self.PUB_BASE_API_URL+"markets/list/")

  def _getConsolData(self):
    return self._unauthenticated_request(self.PUB_BASE_API_URL+"markets/data/")

  def _getCoins(self):
    return self._unauthenticated_request(self.PUB_BASE_API_URL+"coins/list/")



'''
#unauthenticated requests
#List of all markets and the status
market_list_request = _unauthenticated_request('markets/list/')
print market_list_request

#List of all coins and the status
coin_list_request = _unauthenticated_request('coins/list/')
print coin_list_request

#get consolidated market data
consolidate_market_data_request = _unauthenticated_request('markets/data/')
print consolidate_market_data_request


#authenticated requests
user_all_wallets = _authenticated_request('wallet/all/',"getwallets")
print user_all_wallets['wallets']


working_pair = "WDC_BTC"

#placing a new order
new_order_request = _authenticated_request('market/%s/' % (working_pair),"neworder",{'order_type':'buy',
                                                                                         'rate':'0.002123',
                                                                                         'quantity':'1',})
print new_order_request

#get information about an order
get_order_request = _authenticated_request('market/%s/' % (working_pair),"getorder",{'order_id':new_order_request['order']['id']})
print get_order_request

#get list of orders
get_list_of_order_request = _authenticated_request('market/%s/' % (working_pair),"listorders",{'limit':2})

print get_list_of_order_request

for each_order in get_list_of_order_request['orders']:
    print each_order['status']


#cancel an order
order_cancel_request = _authenticated_request('market/%s/' % (working_pair),"cancelorder",{'order_id':get_order_request['order']['id']})
print order_cancel_request
'''