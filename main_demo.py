from models import Movie
from theater import Theater
from booking import Booking


def main():
    # Загрузка фильмов
    movies = Movie.load_from_json("movies.json")
    print("Доступные фильмы:")
    for idx, m in enumerate(movies, start=1):
        print(f"{idx}. {m.title} ({m.duration} мин, рейтинг {m.rating})")

    # Выбор фильма
    choice = int(input("\nВыберите фильм (номер): "))
    selected_movie = movies[choice - 1]

    # Создание зала и добавление сеансов
    theater = Theater("Зал 1", rows=5, cols=5, price_per_seat=1200)
    import random

    # Заранее занятые места (например, 3 случайных)
    for _ in range(5):
        row = random.randint(0, theater.rows - 1)
        col = random.randint(0, theater.cols - 1)
        status = random.choice(["sold", "reserved"])
        theater.seat_map[row][col] = status
    theater.add_session(selected_movie, "18:00")
    theater.add_session(selected_movie, "21:00")

    print("\nДоступные сеансы:")
    for idx, (movie, time) in enumerate(theater.list_sessions(), start=1):
        print(f"{idx}. {movie.title} в {time}")

    # Выбор сеанса
    session_choice = int(input("\nВыберите сеанс (номер): "))
    selected_session = theater.list_sessions()[session_choice - 1][1]

    # Выбор мест
    print("\nПлан мест:")
    for row in theater.show_seat_map():
        print(row)

    seats = []
    while not seats:
        seats_input = input("\nВведите места через запятую "
                            "(например: 1,2 или 1,2;1,3): ")
        for seat_str in seats_input.split(";"):
            row, col = map(int, seat_str.split(","))
            try:
                theater.reserve_seat(row, col)
                seats.append((row, col))
            except ValueError as e:
                print(e)

        if not seats:
            print("\nВы не выбрали ни одного свободного места."
                  " Попробуйте снова.")

    print("\nПлан мест после резервирования:")
    for row in theater.show_seat_map():
        print(row)

    guest = input("\nВведите ваше имя для создания брони: ")

    # Создание брони
    amount = len(seats) * theater.price_per_seat
    booking = Booking(
        booking_id=1,
        movie=selected_movie,
        session=selected_session,
        seats=seats,
        guest=guest,
        amount=amount
    )

    print(f"\nСумма к оплате: {booking.amount} тг.")

    # Цикл оплаты
    while booking.status == "pending":
        try:
            user_amount = float(input("Введите сумму для оплаты "
                                      "(или 0 для отмены): "))
            if user_amount == 0:
                booking.cancel(theater)
                print("Бронь отменена пользователем.")
                break
            booking.confirm(theater, user_amount)
        except ValueError as e:
            print(f"Ошибка: {e}")

        print(f"\nТекущий статус брони: {booking.status}")

    # Итоговый вывод
    print("\nПлан мест после завершения операции:")
    for row in theater.show_seat_map():
        print(row)
    if booking.status == "confirmed":
        print("\nДетали брони:")
        print(f"ID брони: {booking.booking_id}")
        print(f"Фильм: {booking.movie.title}")
        print(f"Время начала: {booking.session}")
        print(f"Зал: {theater.name}")
        print(f"Имя покупателя: {booking.guest}")
        print(f"Количество мест: {len(booking.seats)}")
        print(f"Места: {', '.join([f'{r},{c}' for r, c in booking.seats])}")
        print(f"Сумма оплаты: {booking.amount} тг.")


if __name__ == "__main__":
    main()
