# Generated by Django 4.1 on 2022-09-29 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_profile_display_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_picture',
            field=models.ImageField(default='images/default.png', upload_to='images/'),
        ),
    ]
