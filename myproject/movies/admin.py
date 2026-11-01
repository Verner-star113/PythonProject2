from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, Genre, Season

admin.site.register(Genre)


class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1
    verbose_name = "Сезон"
    verbose_name_plural = "Ссылки на сезоны сериала"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('view_poster', 'title', 'media_type', 'view_progress', 'status', 'rating', 'user',
                    'moderation_status', 'is_recommended', 'view_video_link')
    list_filter = ('moderation_status', 'is_recommended', 'media_type', 'status', 'rating', 'genres', 'user')
    search_fields = ('title', 'review')
    inlines = [SeasonInline]

    # НОВОЕ: Говорим Django, что это поле нельзя редактировать вручную (оно только для вывода картинки)
    readonly_fields = ('form_poster_preview',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        if obj.moderation_status == 'approved':
            obj.is_recommended = True
        elif obj.moderation_status == 'no' and not request.user.is_superuser:
            obj.is_recommended = False
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(models.Q(user=request.user) | models.Q(moderation_status='approved'))

    def get_fieldsets(self, request, obj=None):
        # Добавили 'form_poster_preview' на второе место, сразу после названия!
        main_fields = ['title', 'form_poster_preview', 'media_type', 'status', 'rating', 'genres', 'user',
                       'moderation_status', 'poster_url', 'poster_file']

        if request.user.is_superuser:
            main_fields.insert(7, 'is_recommended')

        if obj:
            active_fields = [f for f in main_fields if f in self.get_fields(request, obj)]
            return [(None, {'fields': active_fields})]

        return [
            ('Основная информация', {
                'fields': tuple(main_fields)
            }),
            ('Настройки для СЕРИАЛОВ (заполнять, если выбран сериал)', {
                'fields': ('current_season', 'current_episode'),
                'description': 'Заполните эти поля, если вы добавляете многосерийный проект.',
            }),
            ('Настройки для ФИЛЬМОВ (заполнять, если выбран фильм)', {
                'fields': ('video_url',),
                'description': 'Вставьте сюда общую ссылку для просмотра полнометражного фильма.',
            }),
        ]

    def get_fields(self, request, obj=None):
        # Добавили 'form_poster_preview' в общий список полей формы
        fields = ['title', 'form_poster_preview', 'media_type', 'status', 'rating', 'genres', 'user',
                  'moderation_status', 'poster_url', 'poster_file']
        if request.user.is_superuser:
            fields.append('is_recommended')

        if obj:
            if obj.media_type == 'series':
                fields += ['current_season', 'current_episode']
            else:
                fields += ['video_url']
        else:
            fields += ['current_season', 'current_episode', 'video_url']
        return fields

    def get_inline_instances(self, request, obj=None):
        if obj and obj.media_type == 'movie':
            return []
        return super().get_inline_instances(request, obj)

    # МАГИЯ КРУПНОГО ПРЕВЬЮ НА ФОРМЕ (высота 300 пикселей, плавно подстраивается):
    def form_poster_preview(self, obj):
        if obj and obj.poster_file:
            return format_html(
                '<img src="{}" style="max-height: 300px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />',
                obj.poster_file.url)
        elif obj and obj.poster_url:
            return format_html(
                '<img src="{}" style="max-height: 300px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />',
                obj.poster_url)
        return "Постер ещё не добавлен. Загрузите файл или вставьте ссылку ниже."

    form_poster_preview.short_description = "Просмотр обложки"

    def view_progress(self, obj):
        if obj.media_type == 'series' and (obj.current_season or obj.current_episode):
            season = f"{obj.current_season} сез." if obj.current_season else "—"
            episode = f"{obj.current_episode} сер." if obj.current_episode else "—"
            return f"{season}, {episode}"
        return "—"

    view_progress.short_description = "Прогресс"

    def view_poster(self, obj):
        if obj.poster_file:
            return format_html('<img src="{}" style="height: 60px; border-radius: 4px;" />', obj.poster_file.url)
        elif obj.poster_url:
            return format_html('<img src="{}" style="height: 60px; border-radius: 4px;" />', obj.poster_url)
        return "Нет фото"

    view_poster.short_description = "Постер"

    def view_video_link(self, obj):
        url = None
        if obj.media_type == 'series' and obj.current_season:
            season_obj = obj.seasons.filter(number=obj.current_season).first()
            if season_obj:
                url = season_obj.video_url
        if not url and obj.video_url:
            url = obj.video_url
        if not url and obj.media_type == 'series' and obj.current_season:
            from django.utils.http import urlencode
            query = f"{obj.title} {obj.current_season} season"
            url = f"https://rutube.ru?{urlencode({'query': query})}"
        if not url:
            return "—"
        return format_html(
            '<a class="button" href="{}" target="_blank" style="background-color: #00a854; color: white; padding: 3px 10px; text-decoration: none; border-radius: 4px;">▶ Смотреть</a>',
            url
        )

    view_video_link.short_description = "Просмотр"

# МЕНЯЕМ НАЗВАНИЕ ВСЕГО САЙТА В ШАПКЕ
admin.site.site_header = "🍿 КиноПоиск На Минималках"

# Меняем заголовок в админ-панели
admin.site.index_title = "Панель управления каталогом"

# Меняем название вкладки в самом браузере
admin.site.site_title = "КиноДневник"
