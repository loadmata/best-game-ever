# Generated by Django 4.2.2 on 2023-06-21 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elogame', '0004_alter_game_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
