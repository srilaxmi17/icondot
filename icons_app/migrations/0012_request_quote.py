# Generated by Django 5.0.2 on 2024-08-12 10:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icons_app', '0011_delete_request_quote'),
    ]

    operations = [
        migrations.CreateModel(
            name='request_quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('description', models.TextField(max_length=200)),
                ('rq_image', models.ImageField(upload_to='re_images/')),
                ('gradient_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icons_app.gradient_category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icons_app.register')),
            ],
        ),
    ]
