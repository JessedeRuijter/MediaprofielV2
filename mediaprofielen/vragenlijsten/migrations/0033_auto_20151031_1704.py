# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0032_auto_20151027_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiel',
            name='completedEnquetes',
        ),
        migrations.RemoveField(
            model_name='profiel',
            name='time',
        ),
        migrations.AddField(
            model_name='profiel',
            name='invulmoment',
            field=models.ForeignKey(related_name='invulmomentprofiel', default=1, to='vragenlijsten.Invulmoment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invulmoment',
            name='organisation',
            field=models.ForeignKey(related_name='organisationInvulMoment', to='vragenlijsten.Organisation'),
        ),
    ]
