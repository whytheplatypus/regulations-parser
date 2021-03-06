# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegulationFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hexhash', models.CharField(default=None, max_length=32, null=True)),
                ('filename', models.CharField(default=None, max_length=512, null=True)),
                ('contents', models.BinaryField()),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]
