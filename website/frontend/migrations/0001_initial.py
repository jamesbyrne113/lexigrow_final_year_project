# Generated by Django 2.2.4 on 2020-03-23 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='WordInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=30)),
                ('pos', models.CharField(max_length=30, verbose_name='part of speech tag')),
                ('level', models.IntegerField()),
            ],
            options={
                'unique_together': {('word', 'pos')},
            },
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('example', models.CharField(max_length=300)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.Details')),
            ],
        ),
        migrations.AddField(
            model_name='details',
            name='word_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.WordInfo'),
        ),
    ]
