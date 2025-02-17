from __future__ import print_function

import gate_api
from gate_api.exceptions import ApiException, GateApiException
from util.coinUtil import convert_coin_name
from private_config import subAccountApiKey, subAccountApiSecret, tempApiKey, tempApiSecret, sizakApiKey, sizakApiSecret

# configuration = gate_api.Configuration(
#     host = "https://api.gateio.ws/api/v4",
#     key = subAccountApiKey,
#     secret = subAccountApiSecret    
# )

# configuration = gate_api.Configuration(
#     host = "https://api.gateio.ws/api/v4",
#     key = tempApiKey,
#     secret = tempApiSecret
# )

configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4",
    key = sizakApiKey,
    secret = sizakApiSecret
)

api_client = gate_api.ApiClient(configuration)
api_instance = gate_api.EarnUniApi(api_client)
spot_api_instance = gate_api.SpotApi(api_client)
unified_api_instance = gate_api.UnifiedApi(api_client)


def get_uni_currencies():
    try:
        # List currencies for lending
        api_response = api_instance.list_uni_currencies()
        print(api_response)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling EarnUniApi->list_uni_currencies: %s\n" % e)

def get_uni_currency(currency):
    try:
        api_response = api_instance.get_uni_currency(currency)
        print(api_response)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling EarnUniApi->get_uni_currency: %s\n" % e)

# 코인 가격 가져오기
def get_candlesticks(currency_pair, interval, limit=None):
    try:
        currency_pair = convert_coin_name(currency_pair)
        if limit is not None:
            api_response = spot_api_instance.list_candlesticks(currency_pair, limit=limit, interval=interval)
        else:
            api_response = spot_api_instance.list_candlesticks(currency_pair, interval=interval)
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
