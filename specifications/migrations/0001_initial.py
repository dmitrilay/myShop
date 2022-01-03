# Generated by Django 3.2.3 on 2021-09-12 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cat', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='ProductSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Товары',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Specifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Имя характеристики',
                'verbose_name_plural': 'Имя характеристики',
            },
        ),
        migrations.CreateModel(
            name='ValuesSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Значения для характеристики',
                'verbose_name_plural': 'Значения для характеристики',
            },
        ),
        migrations.CreateModel(
            name='CharacteristicValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='specifications.categoryproducts')),
                ('name_product', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='specifications.productspec')),
                ('name_spec', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='specifications.specifications')),
                ('name_value', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='specifications.valuesspec')),
            ],
            options={
                'verbose_name': 'Стек характеристик',
                'verbose_name_plural': 'Стек характеристик',
            },
        ),
    ]
