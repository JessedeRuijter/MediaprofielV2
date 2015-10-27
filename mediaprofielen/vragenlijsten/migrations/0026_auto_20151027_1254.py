# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0025_auto_20151027_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enqueteanswer',
            name='time_completed',
        ),
        migrations.AddField(
            model_name='enqueteanswer',
            name='invulmoment',
            field=models.ForeignKey(related_name='invulmoment', default=0, blank=True, to='vragenlijsten.Invulmoment'),
            preserve_default=False,
        ),
    ]
