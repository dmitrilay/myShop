# Generated by Django 3.2.3 on 2021-09-19 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specifications',
            name='participation_filtering',
            field=models.BooleanField(default=False),
        ),
    ]