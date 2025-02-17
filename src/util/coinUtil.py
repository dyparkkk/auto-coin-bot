def convert_coin_name(coin_name):
    if not coin_name.endswith('_USDT'):
        return coin_name + '_USDT'
    return coin_name

