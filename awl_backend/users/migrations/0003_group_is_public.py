# Generated by Django 4.1.3 on 2023-10-13 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]