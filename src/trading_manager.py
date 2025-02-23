import threading
import time
import uuid
from trading import trading

class TradingManager:
    """
    TradingManager는 여러 트레이딩(전략)을 관리합니다.
    1. 각 트레이딩은 고유 id와 메타데이터(coin, amount, position 등)를 가집니다.
    2. 일정 시간마다 모든 트레이딩 함수를 실행하여, 트레이딩 함수가 (True, new_position)을 반환하면 해당 포지션을 업데이트합니다.
    3. get_tradings 함수를 통해 현재 등록된 트레이딩들을 확인할 수 있습니다.
    """
    def __init__(self, interval=43200): # 기본 실행 주기: 12시간 43200
        self.tradings = {}  # key: trading_id, value: dict { trading_func, coin, amount, position, 기타 매개변수 }
        self.interval = interval  # 실행 주기 (초 단위)
        self.timer = None
        self.running = False

    def add_trading(self, coin, amount, position="none", **kwargs):
        """
        새로운 트레이딩을 추가합니다.
        
        Parameters:
            trading_func (function): 실행될 트레이딩 함수. 호출 시 (coin, amount, position, **kwargs)를 인수로 받으며 (bool, new_position)을 반환해야 함.
            coin (str): 코인 이름 (예: 'BTC')
            amount (float): 거래 금액
            position (str): 초기 포지션 ('long', 'short', 'none')
            **kwargs: 그 외 추가 매개변수
        
        Returns:
            trading_id (str): 생성된 트레이딩의 고유 id
        """
        trading_id = str(uuid.uuid4())
        trading_func = trading
        self.tradings[trading_id] = {
            "trading_func": trading_func,
            "coin": coin,
            "amount": amount,
            "position": position,
            "kwargs": kwargs
        }
        print(f"Trading added with id: {trading_id}")
        return trading_id

    def delete_trading(self, trading_id):
        """
        등록된 트레이딩을 고유 id로 삭제합니다.
        """
        if trading_id in self.tradings:
            del self.tradings[trading_id]
            print(f"Trading {trading_id} deleted.")
        else:
            print(f"Trading {trading_id} not found.")

    def get_tradings(self):
        """
        현재 등록된 트레이딩들의 메타데이터를 반환합니다.
        
        Returns:
            dict: { trading_id: { "coin": ..., "amount": ..., "position": ... , ... }, ... }
        """
        return {
            tid: {key: val for key, val in trading.items() if key != "trading_func"}
            for tid, trading in self.tradings.items()
        }

    def run_tradings(self):
        """
        등록된 모든 트레이딩 함수를 실행합니다.
        각 트레이딩 함수가 (True, new_position)을 반환하면, 해당 트레이딩의 포지션을 업데이트합니다.
        """
        print("Executing all tradings...")
        for tid, my_trading in self.tradings.items():
            # result = trading(coin=my_trading["coin"], amount=my_trading["amount"], position=my_trading["position"])
            try:
                # func = trading["trading_func"]
                # 트레이딩 함수 실행: 인수로 coin, amount, position, 추가 매개변수(kwargs)를 전달
                # result = func(trading["coin"], trading["amount"], trading["position"], **trading["kwargs"])
                result = trading(coin=my_trading["coin"], amount=my_trading["amount"], position=my_trading["position"])
                if isinstance(result, tuple) and result[0]:
                    new_position = result[1]
                    my_trading["position"] = new_position
                    print(f"Trading {tid} updated position to: {new_position}")
            except Exception as e:
                print(f"Error executing trading {tid}: {e}")
        if self.running:
            self.timer = threading.Timer(self.interval, self.run_tradings)
            self.timer.start()

    def start(self):
        """
        TradingManager를 시작하여, 일정 주기마다 트레이딩들을 실행합니다.
        """
        if not self.running:
            self.running = True
            print("TradingManager started.")
            self.run_tradings()

    def stop(self):
        """
        TradingManager를 중단합니다.
        """
        self.running = False
        if self.timer:
            self.timer.cancel()
        print("TradingManager stopped.")

# 예시용 트레이딩 함수
def example_trading(coin, amount, position, **kwargs):
    """
    예시 트레이딩 함수.
    coin, amount, position 및 추가 매개변수를 받아 실행 후 (True, new_position)을 반환합니다.
    예시로, 현재 포지션이 'none'이면 'long' 포지션 진입 신호를 발생시키고, 그렇지 않으면 신호 없음으로 반환합니다.
    """
    print(f"Executing trading for {coin} with amount {amount} and current position {position}. Extra: {kwargs}")
    if position == "none":
        return True, "long"
    else:
        return False, position

tm = TradingManager()

# 예시 사용법
if __name__ == "__main__":
    tm = TradingManager(interval=10)  # 데모를 위해 10초 간격으로 실행
    trading_id = tm.add_trading(example_trading, coin="BTC", amount=10, position="none", param1="demo")
    print("Current tradings:", tm.get_tradings())
    # tm.start()
    # time.sleep(30)
    # tm.stop()
