import json

class Movie:
    """
    Класс для хранения информации о фильме.
    """
    def __init__(self, title, duration, rating):
        self.title = title
        self.duration = duration
        self.rating = rating

    @staticmethod
    def load_from_json(filepath: str):
        """
        Загружает список фильмов из JSON файла.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Movie(**movie) for movie in data]




