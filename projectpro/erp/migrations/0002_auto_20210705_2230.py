# Generated by Django 3.2.4 on 2021-07-05 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='faculty_id',
        ),
        migrations.AddField(
            model_name='mark',
            name='subject_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='erp.subject'),
        ),
    ]
