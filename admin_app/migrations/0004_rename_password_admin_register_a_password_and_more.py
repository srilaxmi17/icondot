# Generated by Django 5.0.2 on 2024-08-27 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin_register',
            old_name='password',
            new_name='A_password',
        ),
        migrations.RenameField(
            model_name='admin_register',
            old_name='username',
            new_name='A_username',
        ),
    ]
