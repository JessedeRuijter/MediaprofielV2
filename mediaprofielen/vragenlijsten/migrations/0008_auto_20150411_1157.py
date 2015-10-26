# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vragenlijsten', '0007_auto_20150410_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choiceText', models.CharField(max_length=200)),
                ('question', models.ForeignKey(related_name='choices', to='vragenlijsten.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='question',
            name='qType',
            field=models.CharField(max_length=1, choices=[(b'Y', b'YesNo'), (b'M', b'MultipleChoice'), (b'S', b'Slider')]),
            preserve_default=True,
        ),
    ]
