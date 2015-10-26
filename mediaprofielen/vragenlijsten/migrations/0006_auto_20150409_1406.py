# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0005_account_geslacht'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choicescores',
            name='choice',
        ),
        migrations.DeleteModel(
            name='ChoiceScores',
        ),
        migrations.RemoveField(
            model_name='questionchoice',
            name='question',
        ),
        migrations.DeleteModel(
            name='QuestionChoice',
        ),
        migrations.RemoveField(
            model_name='question',
            name='order',
        ),
        migrations.AddField(
            model_name='question',
            name='offset',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='qType',
            field=models.CharField(max_length=1, choices=[(b'Y', b'YesNo'), (b'M', b'MultipeChoice')]),
            preserve_default=True,
        ),
    ]
