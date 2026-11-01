from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_genres(sender, **kwargs):
    from .models import Genre

    # Расширенный список всех основных жанров кино и сериалов
    popular_genres = [
        "Комедия", "Драма", "Боевик", "Триллер", "Ужасы",
        "Фантастика", "Фэнтези", "Мелодрама", "Детектив",
        "Приключения", "Мультфильм", "Документальный",
        # Новые добавленные жанры:
        "Аниме", "Биография", "Вестерн", "Военный",
        "История", "Криминал", "Мюзикл", "Семейный",
        "Спорт", "Фантасмагория", "Медицинский", "Киберпанк"
    ]

    for genre_name in popular_genres:
        Genre.objects.get_or_create(name=genre_name)


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = "Дневник киномана"

    def ready(self):
        post_migrate.connect(create_default_genres, sender=self)
