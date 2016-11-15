# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='R3SUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=255)),
                ('first_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(unique=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('passwordSettingNeeded', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(to='auth.Group')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission')),
            ],
            options={
                'permissions': (('create_user', 'Create User'), ('change_password', 'Change Password'), ('reset_password', 'Reset Password'), ('assign_group', 'Assign Proup'), ('assign_perms', 'Assign Permission'), ('set_user_active', 'Set User Active'), ('set_user_inactive', 'Set User Inactive')),
            },
        ),
    ]
