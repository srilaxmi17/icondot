# Generated by Django 5.0.2 on 2024-08-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icons_app', '0005_image_image_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
