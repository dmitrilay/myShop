# Generated by Django 3.1.4 on 2020-12-05 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20201205_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='profile',
            field=models.CharField(max_length=50),
        ),
    ]