# Generated by Django 4.1.3 on 2023-04-08 14:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('courses', '0001_initial'),
        ('lecturers', '0001_initial'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LecturerScheduleBlockThrough',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturers.lecturer')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rooms.room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('status', models.CharField(default='NEW', max_length=32)),
                ('file', models.FileField(upload_to='schedule/uploads/')),
                ('progress', models.IntegerField()),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ScheduleBlock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course_name', models.CharField(max_length=128)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('type', models.CharField(max_length=32)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule_blocks', to='courses.course')),
                ('groups', models.ManyToManyField(related_name='schedule_blocks', to='auth.group')),
                ('lecturers', models.ManyToManyField(related_name='schedule_blocks', through='schedule.LecturerScheduleBlockThrough', to='lecturers.lecturer', blank=True)),
                ('rooms', models.ManyToManyField(related_name='schedule_blocks', to='rooms.room', blank=True)),
            ],
            options={
                'ordering': ('-created_at', 'start'),
            },
        ),
        migrations.AddField(
            model_name='lecturerscheduleblockthrough',
            name='schedule_block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.scheduleblock'),
        ),
    ]
