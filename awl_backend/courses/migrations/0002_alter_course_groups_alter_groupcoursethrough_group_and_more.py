# Generated by Django 4.1.3 on 2023-04-08 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_group'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='groups',
            field=models.ManyToManyField(related_name='courses', through='courses.GroupCourseThrough', to='users.group'),
        ),
        migrations.AlterField(
            model_name='groupcoursethrough',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.group'),
        ),
        migrations.AlterField(
            model_name='lecturercoursethrough',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.group'),
        ),
    ]
