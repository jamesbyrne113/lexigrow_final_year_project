# Generated by Django 2.2.4 on 2020-03-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordinfo',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]
