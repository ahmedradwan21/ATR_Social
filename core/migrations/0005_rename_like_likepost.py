# Generated by Django 4.2.1 on 2023-10-29 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_likepost_like'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='Likepost',
        ),
    ]
