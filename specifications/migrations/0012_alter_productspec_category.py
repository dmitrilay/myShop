# Generated by Django 3.2.3 on 2021-12-23 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specifications', '0011_productspec_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspec',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='specifications.categoryproducts'),
        ),
    ]