import numpy as np
from abc import ABC, abstractmethod

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
    


def ma_factory(ma_type: str, period: int) -> MovingAverage:
    """
    이동평균 타입에 따라 적절한 이동평균 계산 객체를 반환하는 팩토리 함수.
    
    Parameters:
        ma_type (str): 이동평균 종류 (예: 'sma', 'ema', ...)
        period (int): 이동평균 계산에 사용할 기간
        
    Returns:
        MovingAverage: 해당 이동평균 계산 객체
    """
    if ma_type.lower() == 'sma':
        return SMA(period)
    # 추후 다른 이동평균 타입 추가 가능 (예: EMA, WMA 등)
    else:
        raise ValueError(f"지원하지 않는 이동평균 타입: {ma_type}")


# 예제 사용법
if __name__ == "__main__":
    # 예시 데이터: 1부터 10까지의 숫자 리스트
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    period = 3

    # 팩토리 함수를 통해 SMA 객체 생성
    ma_calculator = ma_factory("sma", period)
    sma_result = ma_calculator.calculate(data)

    print("SMA 결과:", sma_result)
    # 예상 출력: SMA 결과: [2. 3. 4. 5. 6. 7. 8. 9.]
