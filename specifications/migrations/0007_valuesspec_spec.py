# Generated by Django 3.2.3 on 2021-12-23 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specifications', '0006_specifications_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='valuesspec',
            name='spec',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='specifications.specifications'),
        ),
    ]