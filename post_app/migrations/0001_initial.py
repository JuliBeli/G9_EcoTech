# Generated by Django 4.2.11 on 2025-07-15 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRaw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes_int', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('title', models.TextField(default='New Post', max_length=30)),
                ('image', models.ImageField(blank=True, upload_to='post_images/')),
                ('post_type', models.CharField(choices=[(1, 'admin'), (2, 'user')], default=2, max_length=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post Data Management',
                'db_table': 'post_app_raw',
            },
        ),
    ]
