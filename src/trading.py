from gateIoApi import create_order
from util.coinUtil import convert_coin_name
from trading_strategy.breakthrough import breakthrough_strategy

def trading(coin, amount, position, **kwargs):    

    side = 'none'    
    # 돌파 전략을 통해 신호 발생 여부 및 새 포지션 확인
    isSignal, newPosition = breakthrough_strategy(coin, "1d", amount, position)
    if not isSignal :
        return False, position
    
    if isSignal:
        transition = (position, newPosition)
        mapping = {
            ('long', 'none'): 'sell',
            ('none', 'long'): 'buy',
            ('short', 'none'): 'buy',
            ('short', 'long'): 'buy',
            ('none', 'short'): 'sell'
        }
        side = mapping.get(transition)
        if transition == ('short', 'long'):
            amount = str(float(amount) * 2)
        # 신호 발생 시 포지션 업데이트
        position = newPosition

    order = {
        "text": "t-sampleOrder",                      # 사용자 정의 텍스트 (규칙 준수)
        "currency_pair": convert_coin_name(coin),     # 거래 통화쌍 (예: BTC_USDT)
        "type": "market",                             # 주문 타입: market
        "account": "unified",                         # 계정 타입: unified
        "side": side,                                 # 주문 방향 ('buy' 또는 'sell')
        "amount": amount,                             # 주문 수량
        "time_in_force": "fok",                       # 주문 유효기간 (Fill-Or-Kill)
        "auto_borrow": True,                          # 자동 대출 여부
        "auto_repay": True,                           # 자동 상환 여부
        "status": "open",                             # 초기 주문 상태
    }

    result = create_order(order)
    if result:
        return True, position
    else:
        return False, position

# 예시 호출
if __name__ == "__main__":
    result, pos = trading("BTC", 10)
    print("Order created:", result, "Current position:", pos)
