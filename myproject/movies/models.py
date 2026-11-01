from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    TYPE_CHOICES = [('movie', 'Фильм'), ('series', 'Сериал')]
    STATUS_CHOICES = [('plan', 'Буду смотреть'), ('watching', 'Смотрю'), ('watched', 'Посмотрено')]

    # НОВЫЕ ВАРИАНТЫ: Статусы для системы модерации
    MODERATION_CHOICES = [
        ('no', 'Не предлагалось'),
        ('pending', 'На модерации (предложено пользователем)'),
        ('approved', 'Одобрено и добавлено в общий каталог')
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    media_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='movie', verbose_name="Тип")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='plan', verbose_name="Статус")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], blank=True, null=True,
                                 verbose_name="Моя оценка")
    review = models.TextField(blank=True, verbose_name="Отзыв / Заметка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    genres = models.ManyToManyField(Genre, blank=True, verbose_name="Жанры")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Кто добавил")
    video_url = models.URLField(blank=True, max_length=500, verbose_name="Общая ссылка (для фильмов)")
    is_recommended = models.BooleanField(default=False, verbose_name="Рекомендовано сайтом (видно всем)")
    # Вырежи старый блок постера и вставь этот обновленный:
    poster_url = models.URLField(blank=True, max_length=1000, verbose_name="Ссылка на картинку-постер")

    # НОВОЕ ПОЛЕ: Загрузка файла картинки с компьютера
    # upload_to='posters/' означает, что файлы полетят в папку media/posters/
    poster_file = models.ImageField(upload_to='posters/', blank=True, null=True,
                                    verbose_name="ИЛИ Загрузить файл постера")

    current_season = models.IntegerField(blank=True, null=True, verbose_name="Я на каком сезоне")
    current_episode = models.IntegerField(blank=True, null=True, verbose_name="Я на какой серии")

    # НОВОЕ ПОЛЕ: Статус модерации
    moderation_status = models.CharField(
        max_length=20,
        choices=MODERATION_CHOICES,
        default='no',
        verbose_name="Статус модерации"
    )

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"

    class Meta:
        verbose_name = "Фильм/Сериал"
        verbose_name_plural = "Фильмы и Сериалы"


class Season(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons', verbose_name="Сериал")
    number = models.IntegerField(verbose_name="Номер сезона")
    video_url = models.URLField(max_length=500, verbose_name="Ссылка на плеер для этого сезона")

    def __str__(self):
        return f"{self.movie.title} — {self.number} сезон"

    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны для сериалов"
