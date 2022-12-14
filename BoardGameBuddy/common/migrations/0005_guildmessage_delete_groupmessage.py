# Generated by Django 4.1.3 on 2022-12-11 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('guild', '0009_alter_buddyguild_admins_alter_buddyguild_members'),
        ('common', '0004_requestjoiningguild'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuildMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100)),
                ('date_and_time_of_publication', models.DateTimeField(auto_now_add=True)),
                ('buddy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.buddyprofile')),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild.buddyguild')),
            ],
        ),
        migrations.DeleteModel(
            name='GroupMessage',
        ),
    ]
