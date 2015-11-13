# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0034_auto_20151112_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='invulmoment',
            field=models.ForeignKey(default=1, to='vragenlijsten.Invulmoment'),
            preserve_default=False,
        ),
    ]
