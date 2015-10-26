# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0003_auto_20150409_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='user',
        ),
        migrations.DeleteModel(
            name='Info',
        ),
    ]
