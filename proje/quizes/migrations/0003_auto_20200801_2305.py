# Generated by Django 3.0.8 on 2020-08-01 18:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0002_quiz_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='grades',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=1, max_digits=4), default=[], size=None),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='taken',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(default=False), default=[], size=None),
        ),
    ]
