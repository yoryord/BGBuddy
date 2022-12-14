# Generated by Django 4.1.3 on 2022-12-10 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('guild', '0008_remove_buddyguild_admins_remove_buddyguild_members_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buddyguild',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='admins_set', to='account.buddyprofile'),
        ),
        migrations.AlterField(
            model_name='buddyguild',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members_set', to='account.buddyprofile'),
        ),
    ]
