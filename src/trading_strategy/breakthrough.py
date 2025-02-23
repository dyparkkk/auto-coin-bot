from gateIoApi import get_candlesticks, create_order
from moving_average import ma_factory
from typing import Tuple

def breakthrough_strategy(coin, interval, amount, position, 
                          short_ma_length=20, middle_ma_length=60, long_ma_length=100) -> Tuple[bool, str]:
    """
    돌파전략 (Breakthrough Strategy) 함수

    Parameters:
        coin (str): 코인의 이름 (예: 'BTC', 'ETH' 등)
        interval (str): 거래 기간 (예: '1h', '1d' 등)
        amount (float): 거래에 사용할 구입 금액
        position (str): 현재 포지션 ('long', 'short', 'none')
        short_ma_length (int): 단기 이평선 기간 (default: 80)
        middle_ma_length (int): 중기 이평선 기간 (default: 200)
        long_ma_length (int): 장기 이평선 기간 (default: 400)

    Returns:
        bool: 거래 실행 여부 (조건 만족 시 True, 아니면 False)
    """
    minimum_amount = 1  
    if float(amount) < minimum_amount:
        return False, ''
    
    # 충분한 캔들 데이터를 얻기 위해 long_ma_length 만큼 데이터를 요청 (필요 시 조정)
    data = get_candlesticks(coin, interval, long_ma_length)
    last_prices = [row[2] for row in data]
    
    # 각 이평선 계산 (HMA)
    hma_calculator = ma_factory("hma", short_ma_length)
    hma_short = hma_calculator.calculate(last_prices)
    hma_calculator = ma_factory("hma", middle_ma_length)
    hma_middle = hma_calculator.calculate(last_prices)    
    hma_calculator = ma_factory("hma", long_ma_length)
    hma_long = hma_calculator.calculate(last_prices)
    
    # 각 이평선의 결과 길이가 다를 수 있으므로, 세 개 중 최소 길이를 기준으로 정렬
    min_len = min(len(hma_short), len(hma_middle), len(hma_long))
    if min_len < 2:
        print("비교할 데이터 포인트가 부족합니다.")
        return False, ''
    
    hma_short_aligned = hma_short[-min_len:]
    hma_middle_aligned = hma_middle[-min_len:]
    hma_long_aligned = hma_long[-min_len:]
    
    # 이전과 현재 값 추출
    prev_short = hma_short_aligned[-2]
    curr_short = hma_short_aligned[-1]
    prev_middle = hma_middle_aligned[-2]
    curr_middle = hma_middle_aligned[-1]
    prev_long = hma_long_aligned[-2]
    curr_long = hma_long_aligned[-1]
    
    current_price = float(last_prices[-1])
    print(f"현재 가격: {current_price}")
    print(f"HMA_long - 이전: {prev_long}, 현재: {curr_long}")
    print(f"HMA_short - 이전: {prev_short}, 현재: {curr_short}")
    print(f"HMA_middle - 이전: {prev_middle}, 현재: {curr_middle}")
    
    # [롱 포지션 진입 및 청산 조건]
    # 조건 1: 단기 HMA가 중기 HMA 위에 있고(currently 상승 모멘텀) 
    # 조건 2: 현재 가격이 단기 HMA보다 높으면 롱 진입 (단, 현재 포지션이 long이 아니어야 함)
    if position != "long":
        if curr_short > curr_middle and current_price > curr_short:
            print(f"롱 진입 조건 만족: 단기 HMA({curr_short}) > 중기 HMA({curr_middle}) and 현재 가격({current_price}) > 단기 HMA({curr_short}).")
            return True, "long"
    else:
        today_high = float(data[-1][3])
        today_low = float(data[-1][4])

        N_values = []
        for i in range(1, len(data)):
            today_candle = data[i]
            yesterday_candle = data[i-1]
            option1 = float(today_candle[3]) - float(today_candle[4])
            option2 = abs(float(today_candle[3]) - float(yesterday_candle[2]))
            option3 = abs(float(today_candle[4]) - float(yesterday_candle[2]))
            N_val = max(option1, option2, option3)
            N_values.append(N_val)
        # 최근 20일의 N의 평균
        avg_N = sum(N_values[-20:]) / 20
        recent_high = max(float(candle[3]) for candle in data[-5:])
        if current_price < curr_short or current_price < (recent_high - 2 * avg_N):
            print(f"롱 청산 조건 만족: 현재 가격({current_price}) < 단기 HMA({curr_short}) or 현재 가격({current_price}) < (오늘 고가({today_high}) - 2N({2*avg_N})).")
            return True, "none"
        

        # 이미 롱 포지션인 경우, 단기 HMA 하회 시 청산 조건
        # TODO: 고점 대비 2N 가격이 떨어지면 청산
        if current_price < curr_short:
            print(f"롱 청산 조건 만족: 현재 가격({current_price}) < 단기 HMA({curr_short}).")
            return True, "none"

     # [숏 포지션 진입 및 청산 조건]
    # 1. 단기 HMA와 중기 HMA 간 데드 크로스 발생 시 (이전에는 단기 HMA가 중기 HMA 위에 있었으나, 현재 단기 HMA가 중기 HMA 아래로 내려갔을 경우)
    #    - 현재 포지션이 short이 아니면 숏 포지션 진입
    if position != "short":
        if prev_short > prev_middle and curr_short < curr_middle:
            print(f"데드 크로스 조건 만족 (단기/중기): 이전 HMA_short({prev_short}) > HMA_middle({prev_middle}) and 현재 HMA_short({curr_short}) < HMA_middle({curr_middle}). 숏 포지션 진입.")
            return True, "short"
    else:
        # 2. 이미 숏 포지션인 경우, 단기 HMA와 중기 HMA 간 골든 크로스 발생 시 청산
        if prev_short < prev_middle and curr_short > curr_middle:
            print(f"골든 크로스 조건 만족 (단기/중기): 이전 HMA_short({prev_short}) < HMA_middle({prev_middle}) and 현재 HMA_short({curr_short}) > HMA_middle({curr_middle}). 숏 포지션 청산.")
            return True, "none"
    
    print("조건에 해당하는 신호가 없습니다.")
    return False, 'none'

# 예시 호출
if __name__ == "__main__":
    # 초기 포지션은 'none'
    breakthrough_strategy("BTC", "1h", 10, "none")
