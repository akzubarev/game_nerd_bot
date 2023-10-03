# Generated by Django 4.2.3 on 2023-09-15 13:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event', name='image_link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='event', name='players',
            field=models.ManyToManyField(
                blank=True, null=True, related_name='games',
                to=settings.AUTH_USER_MODEL
            ),
        ),
    ]