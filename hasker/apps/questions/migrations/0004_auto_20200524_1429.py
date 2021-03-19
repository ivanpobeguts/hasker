# Generated by Django 3.0.5 on 2020-05-24 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20200523_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]