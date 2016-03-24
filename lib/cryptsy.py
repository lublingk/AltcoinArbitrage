import string
import _exchange

class cryptsy(_exchange.exchange):
  PUB_BASE_API_URL = "http://pubapi.cryptsy.com/api.php?method="
  PRI_BASE_API_URL = "https://www.cryptsy.com/api/"
  #Cryptsy has static fee percentages, which are the same for all exchanges and has no withdrawal fees, most likely
  BUY_TRADE_FEE_PERCENT = 0.20
  SELL_TRADE_FEE_PERCENT = 0.30
  '''
  AVAILABLE_METHODS = {
                      "public": {"marketdata", "marketdatav2", "orderdata","orderdatav2","singlemarketdata","singleorderdata"},
                      "private": {"getmarkets","getwalletstatus", "mytransactions", "markettrades", "marketorders", "mytrades", "allmytrades", "myorders", "depth", "allmyorders", "createorder", "cancelorder", "cancelmarketorders", "cancelallorders", "calculatefees", "generatenewaddress"}
                      }
  '''
  def _isSuccess(self, json):
    return (json['success'] == "1")

  def _errorMessage(self, json):
    return json['error']

  def _api_query(self, method, req={}):
    if(method == "marketdata" or method == "orderdata" or method == "orderdatav2" or method == "marketdatav2"):
      return self._unauthenticated_request(self.PUB_BASE_API_URL + method)
    elif(method == "singlemarketdata" or method == "singleorderdata"):
      return self._unauthenticated_request(self.PUB_BASE_API_URL + method + '&marketid=' + str(req['marketid']))
    else:
      return self._authenticated_request(self.PRI_BASE_API_URL, method, req)

  #TODO: Improve market available check
  def _fetchNewMarketData(self):
    C = {}
    A = self._getConsolData()
    for x in A['return']:
      startname = string.lower(A['return'][x]["primaryname"])
      endname = string.lower(A['return'][x]["secondaryname"])
      combname = startname + "-" + endname
      C[combname]={
        "name": A['return'][x]["label"],
        "start": startname,
        "end": endname,
        "marketid": A['return'][x]["marketid"],
        "useable": True
      }
      try:
        C[combname]["bestsell"] = {
            "price": A['return'][x]["sellorders"][0]["price"],
            "quantity": A['return'][x]["sellorders"][0]["quantity"]
          }
      except TypeError:
        C[combname]["bestsell"] = {
            "price": None,
            "quantity": None
          }
      try:
        C[combname]["bestbuy"] = {
            "price": A['return'][x]["buyorders"][0]["price"],
            "quantity": A['return'][x]["buyorders"][0]["quantity"]
          }
      except TypeError:
        C[combname]["bestbuy"] = {
            "price": None,
            "quantity": None
          }
    return C
  '''
  #Old Array method
  def _fetchNewMarketData(self):
    C = []
    A = self._getConsolData()
    for x in A['return']:
      C.append({
        "name": A['return'][x]["label"],
        "start": string.lower(A['return'][x]["primaryname"]),
        "end": string.lower(A['return'][x]["secondaryname"]),
        "marketid": A['return'][x]["marketid"],
        "bestsell": {
          "price": _exchange._getElement(_exchange._getElement(A['return'][x]["sellorders"],0),"price"),
          "quantity": _exchange._getElement(_exchange._getElement(A['return'][x]["sellorders"],0),"quantity")
        },
        "bestbuy": {
          "price": _exchange._getElement(_exchange._getElement(A['return'][x]["buyorders"],0),"price"),
          "quantity": _exchange._getElement(_exchange._getElement(A['return'][x]["buyorders"],0),"quantity")
        }
      })
    return C
  '''
  #TODO: Allow Partial dynamic fetching of coin data(just coin names) 
  '''
  #ADD More elements if needed(time,confirmation,etc)
  def _fetchNewCoinData(self):
    C = {}
    A = self._getCoins()
    for x in range(0, len(A)):
      name=string.lower(A[x]["name"])
      C[name]={
        "buy_trade_fee_percent": BUY_TRADE_FEE_PERCENT,
        "sell_trade_fee_percent": SELL_TRADE_FEE_PERCENT,
        "withdrawal_fee": A[x]["withdrawalfee"],
        "coinid": A[x]["code"]
      }
    return C
  '''


  def _getMarkets(self):
    return self._api_query("marketdatav2")

  def _getConsolData(self):
    return self._api_query("orderdatav2")

  #Need to figure out a good way to get cryptsy's coin data.
  def _getCoins(self):
    return self._api_query("getwalletstatus")