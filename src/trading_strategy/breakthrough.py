from gateIoApi import get_candlesticks
from moving_average import ma_factory

def breakthrough_strategy(코인이름, 기간, 구입금액, 포지션):
    """
    돌파전략 (Breakthrough Strategy) 함수

    Parameters:
        코인이름 (str): 코인의 이름 (예: 'BTC', 'ETH' 등)
        기간 (str): 거래 기간 (예: '1h', '1d' 등)
        구입금액 (float): 거래에 사용할 구입 금액
        포지션 (str): 현재 포지션 ('long', 'short', 'none')

    Returns:
        bool: 거래 성공 여부 (True: 성공, False: 실패)
    """
    minimum_amount = 1  
    if 구입금액 < minimum_amount:
        return False
    
    data = get_candlesticks(코인이름, 기간)
    last_prices = [row[2] for row in data]

    hma_calculator = ma_factory("hma", 20)
    hma_20 = hma_calculator.calculate(last_prices)
    hma_calculator = ma_factory("hma", 50)
    hma_50 = hma_calculator.calculate(last_prices)
    
    # HMA 계산 결과는 'valid' 모드로 구해지므로, 데이터 길이가 period에 따라 달라짐
    if len(hma_50) == 0:
        print("데이터 길이가 부족합니다.")
        return False

    # 20일 HMA를 50일 HMA와 비교하기 위해, 마지막 부분만 추출
    hma_20_aligned = hma_20[-len(hma_50):]
    print("HMA20:", hma_20_aligned)
    
    if len(hma_50) < 2:
        print("비교할 데이터 포인트가 부족합니다.")
        return False

    # 이전과 현재 HMA 값 추출
    prev_short = hma_20_aligned[-2]
    prev_long = hma_50[-2]
    curr_short = hma_20_aligned[-1]
    curr_long = hma_50[-1]
    
    # 골든 크로스 & 데드 크로스 판별
    if prev_short < prev_long and curr_short > curr_long:
        print(f"이전 값 - HMA20: {prev_short}, HMA50: {prev_long}")
        print(f"현재 값 - HMA20: {curr_short}, HMA50: {curr_long}")
        if 포지션 == "long":
            print("이미 롱 포지션입니다. 골든 크로스 발생해도 아무 행동을 하지 않습니다.")
            return False
        else:
            print("골든 크로스 발생 - 롱 포지션 진입")
            # 롱 포지션 진입 로직 추가
            포지션 = "long"
    elif prev_short > prev_long and curr_short < curr_long:
        if 포지션 == "short":
            print("이미 숏 포지션입니다. 데드 크로스 발생해도 아무 행동을 하지 않습니다.")
        else:
            print("데드 크로스 발생 - 숏 포지션 진입")
            # 숏 포지션 진입 로직 추가
            포지션 = "short"
    else:
        print("크로스 발생 없음")
    
    # 거래 성공 여부를 리턴하는 로직은 전략에 따라 추가 구현 가능
    return True

# 예시 호출
if __name__ == "__main__":
    # 초기 포지션은 'none'
    breakthrough_strategy("BTC", "1h", 10, "none")
