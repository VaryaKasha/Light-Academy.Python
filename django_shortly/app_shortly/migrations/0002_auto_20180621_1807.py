# Generated by Django 2.0.6 on 2018-06-21 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_shortly', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Urls',
            new_name='UrlObject',
        ),
    ]