# Generated by Django 3.0.3 on 2020-04-09 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_lexigrowuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lexigrowuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
    ]
