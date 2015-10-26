# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0018_auto_20150507_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organisation',
            name='owners',
            field=models.ManyToManyField(related_name='owners', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
