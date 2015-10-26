# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0002_auto_20150409_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='actief',
        ),
    ]
