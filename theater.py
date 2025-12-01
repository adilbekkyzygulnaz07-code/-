class Theater:
    """
    Класс для управления залом и сеансами.
    """
    def __init__(self, name: str, rows: int, cols: int, price_per_seat: float):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.price_per_seat = price_per_seat
        self.seat_map = [["free" for _ in range(cols)] for _ in range(rows)]
        self.schedule = []  # список кортежей (Movie, time)

    def add_session(self, movie, time: str):
        """Добавить сеанс в расписание."""
        self.schedule.append((movie, time))

    def list_sessions(self):
        """Вернуть список доступных сеансов."""
        return self.schedule

    def show_seat_map(self):
        """Показать текущее состояние мест."""
        return self.seat_map

    def reserve_seat(self, row: int, col: int):
        """Резервировать место, если оно свободно. Если занято — выбросить ValueError."""
        if self.seat_map[row][col] == "free":
            self.seat_map[row][col] = "reserved"
        elif self.seat_map[row][col] == "reserved":
            raise ValueError(f"⚠️ Место {row},{col} уже зарезервировано.")
        elif self.seat_map[row][col] == "sold":
            raise ValueError(f"⚠️ Место {row},{col} уже продано.")

    def free_seat(self, row: int, col: int):
        """Освободить место (например, при отмене брони)."""
        self.seat_map[row][col] = "free"

    def confirm_seat(self, row: int, col: int):
        """Перевести место в статус sold (оплачено)."""
        if self.seat_map[row][col] != "reserved":
            raise ValueError("Место должно быть зарезервировано перед подтверждением")
        self.seat_map[row][col] = "sold"
