# Generated by Django 4.1.7 on 2023-03-25 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_remove_interest_interest1_interest_interest_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isFriend', models.BooleanField(default=False)),
            ],
        ),
    ]
