import random

def process_payment(amount: float) -> bool:
    """
    Фейковая функция оплаты.
    Возвращает True/False случайным образом.
    """
    if amount < 0:
        raise ValueError("Сумма оплаты не может быть отрицательной")
    return random.random() < 0.8


