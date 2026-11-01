from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    # Если пользователь заходит на главную страницу, автоматически перенаправляем его в админку
    path('', RedirectView.as_view(url='/admin/', permanent=False), name='index'),
    path('admin/', admin.site.core.admin_views if hasattr(admin.site, 'core') else admin.site.urls),
]

# Подключаем раздачу медиафайлов (картинок) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
