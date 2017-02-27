# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 21:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelves', '0002_bookshelf_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=60)),
                ('bookshelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshelves.Bookshelf')),
            ],
        ),
    ]
