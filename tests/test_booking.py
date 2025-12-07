import unittest
from theater import Theater
from booking import Booking
from payments import process_payment


class TestTheater(unittest.TestCase):

    def test_add_session(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.add_session("Movie1", "18:00")
        self.assertEqual(t.list_sessions(), [("Movie1", "18:00")])

    def test_list_sessions(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.add_session("Movie1", "18:00")
        t.add_session("Movie2", "21:00")
        self.assertEqual(len(t.list_sessions()), 2)

    def test_show_seat_map(self):
        t = Theater("Zal1", 5, 5, 1200)
        seat_map = t.show_seat_map()
        self.assertEqual(seat_map[0][0], "free")
        self.assertEqual(seat_map[1][1], "free")

    def test_reserve_seat(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.reserve_seat(0, 0)
        self.assertEqual(t.seat_map[0][0], "reserved")

    def test_reserve_seat_reserved(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.reserve_seat(0, 0)
        with self.assertRaises(ValueError):
            t.reserve_seat(0, 0)

    def test_free_seat(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.reserve_seat(0, 1)
        t.free_seat(0, 1)
        self.assertEqual(t.seat_map[0][1], "free")

    def test_confirm_seat(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.reserve_seat(1, 1)
        t.confirm_seat(1, 1)
        self.assertEqual(t.seat_map[1][1], "sold")

    def test_confirm_seat_no_reserved(self):
        t = Theater("Zal1", 5, 5, 1200)
        with self.assertRaises(ValueError):
            t.confirm_seat(0, 0)


class TestBooking(unittest.TestCase):

    def test_booking_creation(self):
        b = Booking(1, "Movie", "18:00", [(0, 0)], "f", 1200)
        self.assertEqual(b.status, "pending")

    def test_validate_reserved_seats(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.reserve_seat(0, 0)

        b = Booking(1, "Movie", "18:00", [(0, 0)], "f", 1200)
        b.validate_reserved_seats(t)  # не должно быть ошибки

    def test_validate_reserved_seats_fail(self):
        t = Theater("Zal1", 5, 5, 1200)
        b = Booking(1, "Movie", "18:00", [(1, 1)], "f", 1200)

        with self.assertRaises(ValueError):
            b.validate_reserved_seats(t)

    def test_cancel(self):
        t = Theater("Zal1", 5, 5, 1200)
        t.reserve_seat(1, 1)

        b = Booking(1, "Movie", "18:00", [(1, 1)], "f", 1200)
        b.cancel(t)

        self.assertEqual(b.status, "cancelled")
        self.assertEqual(t.seat_map[1][1], "free")


class TestPayments(unittest.TestCase):

    def test_payment_positive(self):
        result = process_payment(100)
        self.assertIn(result, [True, False])

    def test_payment_zero(self):
        result = process_payment(0)
        self.assertIn(result, [True, False])

    def test_payment_negative(self):
        with self.assertRaises(ValueError):
            process_payment(-5)


if __name__ == "__main__":
    unittest.main()
