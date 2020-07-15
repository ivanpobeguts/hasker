# Generated by Django 3.0.7 on 2020-07-15 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20200714_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='correct_for_question', to='questions.Answer'),
        ),
    ]
