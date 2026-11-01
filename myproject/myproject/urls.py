from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.core.admin_views if hasattr(admin.site, 'core') else admin.site.urls),
]

# Подключаем раздачу медиафайлов (картинок) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
