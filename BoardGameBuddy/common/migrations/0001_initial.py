# Generated by Django 4.1.3 on 2022-12-04 13:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0001_initial'),
        ('account', '0001_initial'),
        ('guild', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100)),
                ('date_and_time_of_publication', models.DateTimeField(auto_now_add=True)),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild.buddyguild')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.buddyprofile')),
            ],
        ),
        migrations.CreateModel(
            name='GameRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1.0, message='Rating could not be lower than 1.0.'), django.core.validators.MaxValueValidator(10.0, message='Rating could not be bigger than 10.0.')])),
                ('buddy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.buddyprofile')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
        migrations.CreateModel(
            name='GameLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buddy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.buddyprofile')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
        migrations.CreateModel(
            name='GameComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300)),
                ('date_and_time_of_publication', models.DateTimeField(auto_now_add=True)),
                ('buddy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.buddyprofile')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
    ]
