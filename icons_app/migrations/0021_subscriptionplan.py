# Generated by Django 5.0.2 on 2024-08-23 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icons_app', '0020_sub_gradient_category_featured_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('personal', 'Personal'), ('team', 'Team')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
