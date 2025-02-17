import numpy as np
from abc import ABC, abstractmethod
import math

class MovingAverage(ABC):
    """
    이동평균 계산을 위한 베이스 추상 클래스.
    period: 이동평균 계산에 사용할 기간(윈도우 크기)
    """
    def __init__(self, period: int):
        if period <= 0:
            raise ValueError("period는 0보다 커야 합니다.")
        self.period = period

    @abstractmethod
    def calculate(self, data) -> np.ndarray:
        """
        data: 숫자형 값들이 담긴 리스트 또는 NumPy 배열
        반환값: 계산된 이동평균 결과 (NumPy 배열)
        """
        pass

class SMA(MovingAverage):
    """
    단순 이동평균(Simple Moving Average)을 계산하는 클래스.
    NumPy의 np.convolve를 이용하여 효율적으로 계산합니다.
    """
    def calculate(self, data) -> np.ndarray:
        # data를 NumPy 배열로 변환
        data = np.asarray(data, dtype=float)
        if data.size < self.period:
            # 데이터 개수가 period보다 작으면 빈 배열 반환
            return np.array([])
        
        # 단순 이동평균 계산:
        # weights는 period 길이의 동일 가중치 배열
        weights = np.ones(self.period) / self.period
        # 'valid' 모드를 사용하면 계산 가능한 구간만 결과에 포함됨
        sma_values = np.convolve(data, weights, mode='valid')
        return sma_values

class HMA(MovingAverage):
    """
    Hull Moving Average (HMA)를 계산하는 클래스.
    
    HMA 계산 방법:
        HMA = WMA(2 * WMA(data, n/2) - WMA(data, n), sqrt(n))
    여기서 n은 period, WMA는 가중치 이동평균.
    """
    def calculate(self, data) -> np.ndarray:
        data = np.asarray(data, dtype=float)
        n = self.period
        if data.size < n:
            return np.array([])
        
        # WMA를 계산하는 내부 함수
        # 주어진 period에 대해, 가장 최근 값에 높은 가중치: [1, 2, ..., period]
        # np.convolve는 두 번째 인자를 뒤집어 적용하므로, 
        # np.arange(period, 0, -1) 를 사용하면 올바른 결과를 얻을 수 있음.
        def wma(arr, period):
            weights = np.arange(period, 0, -1)
            return np.convolve(arr, weights, mode='valid') / (period * (period + 1) / 2)
        
        # n/2 및 sqrt(n) 계산 (정수값으로 변환)
        n_half = int(n / 2)
        n_sqrt = int(math.sqrt(n))
        if n_half <= 0:
            n_half = 1
        if n_sqrt <= 0:
            n_sqrt = 1

        # WMA 계산:
        wma_full = wma(data, n)            # 길이: len(data) - n + 1
        wma_half = wma(data, n_half)         # 길이: len(data) - n_half + 1
        
        # 두 WMA의 길이를 맞추기 위해, wma_half의 뒤쪽 부분을 사용
        # 원하는 길이는 len(data) - n + 1
        start_index = n - n_half  # (len(wma_half) - (len(data)-n+1)) 계산 결과
        wma_half_truncated = wma_half[start_index:]
        
        # 두 WMA가 정렬된 길이로 계산되었는지 확인 (디버깅용)
        if wma_half_truncated.size != wma_full.size:
            raise ValueError("WMA 길이 정렬에 문제가 발생했습니다.")
        
        # 두 WMA를 이용해 중간 값을 계산: diff = 2 * WMA(data, n/2) - WMA(data, n)
        diff = 2 * wma_half_truncated - wma_full
        
        # 최종 HMA 계산: diff에 대해 WMA를 적용
        hma = wma(diff, n_sqrt)
        return hma

def ma_factory(ma_type: str, period: int) -> MovingAverage:
    """
    이동평균 타입에 따라 적절한 이동평균 계산 객체를 반환하는 팩토리 함수.
    
    Parameters:
        ma_type (str): 이동평균 종류 (예: 'sma', 'ema', 'hma', ...)
        period (int): 이동평균 계산에 사용할 기간
        
    Returns:
        MovingAverage: 해당 이동평균 계산 객체
    """
    if ma_type.lower() == 'sma':
        return SMA(period)
    elif ma_type.lower() == 'hma':
        return HMA(period)
    else:
        raise ValueError(f"지원하지 않는 이동평균 타입: {ma_type}")


# 예제 사용법
if __name__ == "__main__":
    # 예시 데이터: 1부터 100까지의 숫자 리스트
    data = np.arange(1, 101)
    period = 20

    # SMA 계산 예시
    sma_calculator = ma_factory("sma", period)
    sma_result = sma_calculator.calculate(data)
    print("SMA 결과:", sma_result)

    # HMA 계산 예시
    hma_calculator = ma_factory("hma", period)
    hma_result = hma_calculator.calculate(data)
    print("HMA 결과:", hma_result)
