# Generated by Django 2.2 on 2019-04-18 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20190418_0148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='score',
        ),
    ]
