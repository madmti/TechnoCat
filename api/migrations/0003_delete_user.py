# Generated by Django 4.2.5 on 2023-09-13 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_contra'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
