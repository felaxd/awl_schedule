# Generated by Django 4.1.3 on 2023-10-13 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecturers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
