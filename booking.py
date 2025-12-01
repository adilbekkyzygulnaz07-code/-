from payments import process_payment

class Booking:
    STATUSES = ("pending", "confirmed", "cancelled", "expired")

    def __init__(self, booking_id: int, movie, session: str, seats: list, guest: str, amount: float):
        if not seats:
            raise ValueError("Нельзя создать бронь без мест")
        self.booking_id = booking_id
        self.movie = movie
        self.session = session
        self.seats = seats
        self.guest = guest
        self.amount = amount
        self.status = "pending"

    def validate_reserved_seats(self, theater):
        """Проверка: все места из брони должны быть в статусе reserved."""
        for row, col in self.seats:
            if theater.seat_map[row][col] != "reserved":
                raise ValueError(f"Место {row},{col} не зарезервировано")

    def confirm(self, theater, user_amount: float):
        """Подтверждение брони: проверка суммы и перевод мест в sold."""
        if user_amount != self.amount:
            print("❌ Ошибка: введённая сумма не совпадает с требуемой.")
            self.status = "pending"
            return

        # Проверяем, что все места действительно reserved
        self.validate_reserved_seats(theater)

        # Вызываем процесс оплаты
        try:
            success = process_payment(user_amount)
        except ValueError as e:
            print(f"❌ Ошибка: {e}")
            self.status = "pending"
            return

        if success:
            self.status = "confirmed"
            for row, col in self.seats:
                theater.confirm_seat(row, col)
        else:
            print("❌ Оплата не прошла.")
            self.status = "pending"

    def cancel(self, theater):
        """Отмена брони и освобождение мест."""
        for row, col in self.seats:
            theater.free_seat(row, col)
        self.status = "cancelled"
