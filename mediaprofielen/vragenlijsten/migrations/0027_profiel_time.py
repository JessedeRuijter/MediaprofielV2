# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0026_auto_20151027_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiel',
            name='time',
            field=models.DateField(default=datetime.datetime(2015, 10, 27, 11, 59, 42, 778024, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
