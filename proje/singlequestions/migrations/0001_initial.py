# Generated by Django 3.0.8 on 2020-07-24 10:19

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Singlequestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('answers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=300), size=None)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.Quiz')),
            ],
        ),
    ]
