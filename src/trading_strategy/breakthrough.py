from gateIoApi import get_candlesticks

def breakthrough_strategy( 코인이름, 기간, 구입금액, 포지션):
    """
    돌파전략 (Breakthrough Strategy) 함수

    Parameters:
        코인이름 (str): 코인의 이름 (예: 'BTC', 'ETH' 등)
        기간 (str): 거래 기간 (예: '1h', '1d' 등)
        구입금액 (float): 거래에 사용할 구입 금액
        이평선 기준(str) : 20, 50... 
        포지션 (str): 거래 유형 ('long' 또는 'short')

    Returns:
        bool: 거래 성공 여부 (True: 성공, False: 실패)
    """
    minimum_amount = 1  
    if 구입금액 < minimum_amount:
        return False
    
    data = get_candlesticks(코인이름, 기간)
    last_prices = [row[2] for row in data]
    


    