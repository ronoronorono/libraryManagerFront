# Generated by Django 5.1.2 on 2024-11-14 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.CharField(max_length=13, primary_key=True, serialize=False),
        ),
    ]
