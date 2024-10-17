# Generated by Django 5.1.2 on 2024-10-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuserprofile',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='customuserprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
