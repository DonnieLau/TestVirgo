# Generated by Django 3.2.5 on 2021-10-14 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0003_auto_20211012_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_step',
            name='api_login',
            field=models.CharField(max_length=10, null=True),
        ),
    ]