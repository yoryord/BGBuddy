# Generated by Django 4.1.3 on 2022-12-17 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_guildmessage_delete_groupmessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guildmessage',
            options={'ordering': ['-date_and_time_of_publication']},
        ),
    ]
