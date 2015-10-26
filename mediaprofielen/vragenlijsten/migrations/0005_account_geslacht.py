# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0004_auto_20150409_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='geslacht',
            field=models.CharField(default='M', max_length=b'1', choices=[(b'M', b'Man'), (b'V', b'Vrouw')]),
            preserve_default=False,
        ),
    ]
