from __future__ import print_function

import gate_api
from gate_api.exceptions import ApiException, GateApiException

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)


api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.EarnUniApi(api_client)
spot_api_instance = gate_api.SpotApi(api_client)

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

def get_candlesticks(currency_pair, interval, limit=None):
    try:
        if limit is not None:
            api_response = spot_api_instance.list_candlesticks(currency_pair, limit=limit, interval=interval)
        else:
            api_response = spot_api_instance.list_candlesticks(currency_pair, interval=interval)
        print(api_response)
        return api_response
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_candlesticks: %s\n" % e)