# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0015_profiletext_profiel'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquete',
            name='locked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
