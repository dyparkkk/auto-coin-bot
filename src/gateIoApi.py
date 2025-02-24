from __future__ import print_function

import gate_api
from gate_api.exceptions import ApiException, GateApiException
from util.coinUtil import convert_coin_name
from private_config import subAccountApiKey, subAccountApiSecret, tempApiKey, tempApiSecret, sizakApiKey, sizakApiSecret, oracleApiKey, oracleApiSecret

key=oracleApiKey
secret=oracleApiSecret
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4",
    key = key,
    secret = secret
)

api_client = gate_api.ApiClient(configuration)
api_instance = gate_api.EarnUniApi(api_client)
spot_api_instance = gate_api.SpotApi(api_client)
unified_api_instance = gate_api.UnifiedApi(api_client)

# 코인 가격 가져오기
def get_candlesticks(currency_pair:str, interval:str, limit:int=100):
    try:
        currency_pair = convert_coin_name(currency_pair)
        api_response = spot_api_instance.list_candlesticks(currency_pair, limit=limit, interval=interval)
        return api_response
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_candlesticks: %s\n" % e)

# account api
def get_list_unified_accounts():
    try:
        api_response = unified_api_instance.list_unified_accounts()
        return api_response
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling UnifiedApi->list_unified_accounts: %s\n" % e)

 
x_gate_exptime = 10000 # int | Specify the expiration time (milliseconds); if the GATE receives the request time greater than the expiration time, the request will be rejected (optional)
def create_order(order):
    try:
    # Create an order
        api_response = spot_api_instance.create_order(order)
        print(api_response)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->create_order: %s\n" % e)

