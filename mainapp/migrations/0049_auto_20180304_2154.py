# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-05 03:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0048_auto_20180304_2149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='number',
            new_name='course_number',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='section',
            new_name='course_subject',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='subject',
            new_name='section_id',
        ),
    ]