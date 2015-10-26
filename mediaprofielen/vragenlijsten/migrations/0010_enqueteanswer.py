# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vragenlijsten', '0009_remove_answer_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnqueteAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answers', models.CommaSeparatedIntegerField(max_length=1000)),
                ('time_completed', models.DateTimeField()),
                ('enquete', models.ForeignKey(to='vragenlijsten.Enquete')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
