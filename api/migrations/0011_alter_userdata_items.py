# Generated by Django 4.2.5 on 2023-10-19 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_userdata_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='Items',
            field=models.CharField(default='{}', max_length=9999),
        ),
    ]