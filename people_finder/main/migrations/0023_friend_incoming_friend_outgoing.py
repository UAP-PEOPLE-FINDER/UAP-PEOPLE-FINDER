# Generated by Django 4.1.7 on 2023-03-25 20:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0022_remove_friend_incoming_remove_friend_outgoing'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='incoming',
            field=models.ManyToManyField(related_name='incoming', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friend',
            name='outgoing',
            field=models.ManyToManyField(related_name='outgoing', to=settings.AUTH_USER_MODEL),
        ),
    ]
