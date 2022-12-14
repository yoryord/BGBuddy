# Generated by Django 4.1.3 on 2022-12-04 13:19

import BoardGameBuddy.account.cust_validators
import BoardGameBuddy.account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuddyAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user email',
                'verbose_name_plural': 'user emails',
            },
            managers=[
                ('objects', BoardGameBuddy.account.models.BuddyManager()),
            ],
        ),
        migrations.CreateModel(
            name='BuddyProfile',
            fields=[
                ('nickname', models.CharField(max_length=15, null=True, validators=[django.core.validators.MinLengthValidator(2, message='Nickname must consist of minimum 2 chars'), BoardGameBuddy.account.cust_validators.validate_nickname_chars])),
                ('age', models.PositiveIntegerField(null=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, validators=[BoardGameBuddy.account.cust_validators.validate_names_chars])),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, validators=[BoardGameBuddy.account.cust_validators.validate_names_chars])),
                ('personal_interests', models.TextField(blank=True, help_text='(max 300 characters)', max_length=300, null=True)),
                ('is_public', models.BooleanField(default=True, help_text='Share your personal info')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='mediafiles/profile_photo/', validators=[BoardGameBuddy.account.cust_validators.validate_file_size])),
                ('account_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]