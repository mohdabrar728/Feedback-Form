# Generated by Django 3.2.4 on 2021-08-30 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_tempmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempmodel',
            name='options',
            field=models.TextField(null=True),
        ),
    ]