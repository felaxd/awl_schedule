# Generated by Django 4.1.3 on 2023-04-08 11:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lecturers', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LecturerCourseThrough',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lecture_hours', models.IntegerField(default=0)),
                ('exercises_hours', models.IntegerField(default=0)),
                ('laboratory_hours', models.IntegerField(default=0)),
                ('seminary_hours', models.IntegerField(default=0)),
                ('project_hours', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturers.lecturer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupCourseThrough',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lecture_hours', models.IntegerField(default=0)),
                ('exercises_hours', models.IntegerField(default=0)),
                ('laboratory_hours', models.IntegerField(default=0)),
                ('seminary_hours', models.IntegerField(default=0)),
                ('project_hours', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='course',
            name='groups',
            field=models.ManyToManyField(related_name='courses', through='courses.GroupCourseThrough', to='auth.group'),
        ),
        migrations.AddField(
            model_name='course',
            name='lecturers',
            field=models.ManyToManyField(related_name='courses', through='courses.LecturerCourseThrough', to='lecturers.lecturer'),
        ),
    ]
