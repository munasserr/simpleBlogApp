# Generated by Django 4.2.11 on 2024-03-16 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogPost',
            new_name='Post',
        ),
    ]