import unittest
from theater import Theater
from booking import Booking
from payments import process_payment


class TestBookingSystem(unittest.TestCase):

    def setUp(self):
        """Создаем базовые объекты для тестов."""
        self.theater = Theater("Zal1", rows=3, cols=3, price_per_seat=1200)
        self.movie = "Movie1"
        self.session = "18:00"

    def test_successful_reservation_and_confirm(self):
        # Резервируем место
        self.theater.reserve_seat(0, 0)
        self.assertEqual(self.theater.seat_map[0][0], "reserved")

        booking = Booking(
            booking_id=1,
            movie=self.movie,
            session=self.session,
            seats=[(0, 0)],
            guest="l",
            amount=1200
        )

        booking.confirm(self.theater, user_amount=1200)

        self.assertEqual(booking.status, "confirmed")
        self.assertEqual(self.theater.seat_map[0][0], "sold")

    def test_double_reservation_raises(self):
        # Первое резервирование ок
        self.theater.reserve_seat(1, 1)

        # Второе резервирование того же места нельзя
        with self.assertRaises(ValueError):
            self.theater.reserve_seat(1, 1)

    def test_cancel_booking_frees_seats(self):
        self.theater.reserve_seat(2, 2)

        booking = Booking(
            booking_id=2,
            movie=self.movie,
            session=self.session,
            seats=[(2, 2)],
            guest="f",
            amount=12000
        )

        # Отмена брони
        booking.cancel(self.theater)

        self.assertEqual(booking.status, "cancelled")
        self.assertEqual(self.theater.seat_map[2][2], "free")

    def test_create_booking_empty_seats_error(self):
        """при создание брони без мест выйдет ValueError"""
        with self.assertRaises(ValueError):
            Booking(
                booking_id=3,
                movie=self.movie,
                session=self.session,
                seats=[],
                guest="а",
                amount=1200
            )

    def test_confirm_wrong_booking_seat_error(self):
        """
        Попытка подтвердить место, которое зарезервировон другим.
        Имитируем так: место не помечено как зарезервированным ошибка.
        """
        # Место свободное, не reserved
        booking = Booking(
            booking_id=4,
            movie=self.movie,
            session=self.session,
            seats=[(0, 1)],
            guest="а",
            amount=1200
        )

        with self.assertRaises(ValueError):
            booking.confirm(self.theater, user_amount=1200)


if __name__ == "__main__":
    unittest.main()
