# Generated by Django 4.1.3 on 2022-12-10 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_rename_band_groupmessage_guild'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GameComment',
        ),
    ]
