# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0017_auto_20150430_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='csvMembers',
            field=models.FileField(default=0, upload_to=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organisation',
            name='csvOwners',
            field=models.FileField(default='Hallo', upload_to=b''),
            preserve_default=False,
        ),
    ]
