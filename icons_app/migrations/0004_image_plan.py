# Generated by Django 5.0.2 on 2024-08-08 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icons_app', '0003_category_category_shape_category_type_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='image_plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_plan', models.CharField(max_length=25)),
            ],
        ),
    ]
