# Generated by Django 2.0.6 on 2018-06-26 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movienews_app', '0002_auto_20180626_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviemodel',
            name='duration',
        ),
    ]
