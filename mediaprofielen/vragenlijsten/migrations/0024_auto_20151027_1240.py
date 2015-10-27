# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0023_auto_20150513_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invulmoment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateField()),
                ('enquete', models.ForeignKey(related_name='enquete', to='vragenlijsten.Enquete')),
            ],
        ),
        migrations.AddField(
            model_name='organisation',
            name='invulmoment',
            field=models.ManyToManyField(related_name='invulmomenten', to='vragenlijsten.Invulmoment', blank=True),
        ),
    ]
