# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0024_auto_20151027_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='invulmoment',
        ),
        migrations.AddField(
            model_name='invulmoment',
            name='organisation',
            field=models.ForeignKey(related_name='organisation', default=0, to='vragenlijsten.Organisation'),
            preserve_default=False,
        ),
    ]
