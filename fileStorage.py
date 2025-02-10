# storage.py

def save_input_values(value1, value2):
    """
    두 개의 입력값을 파일에 저장하는 함수입니다.
    호출될 때마다 'saved_input.txt' 파일에 두 값이 한 줄에 저장됩니다.
    """
    with open("./output/saved_input.txt", "a", encoding="utf-8") as f:
        # 값들을 쉼표로 구분하여 저장합니다.
        f.write(f"{value1}, {value2}\n")
