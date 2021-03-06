# Generated by Django 3.0.8 on 2020-07-24 10:19

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('descriprion', models.TextField(blank=True)),
                ('number', models.IntegerField()),
                ('quizcreated_date', models.DateTimeField(default=datetime.datetime.now)),
                ('quizduration', models.IntegerField(default=2)),
                ('grades', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=1, max_digits=4), size=None)),
                ('myclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.Class')),
            ],
        ),
    ]
