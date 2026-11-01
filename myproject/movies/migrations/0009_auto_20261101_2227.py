from django.db import migrations

def create_admin_user(apps, schema_editor):
    from django.contrib.auth.models import User
    # Проверяем, если админа еще нет, создаем его
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '1234509876admin337')

class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0002_movie_poster_file'), # Убедись, что тут указано имя твоей прошлой миграции
    ]
    operations = [
        migrations.RunPython(create_admin_user),
    ]
