from django.db import models


class CategoryProducts(models.Model):
    name_cat = models.CharField(max_length=100, unique=True, verbose_name="название")

    def __str__(self):
        return self.name_cat

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категория'


class Specifications(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    participation_filtering = models.BooleanField(default=False, db_index=True)
    priority_spec = models.CharField(max_length=10, default=99, db_index=True, verbose_name='приоритет')
    category = models.ForeignKey('CategoryProducts', on_delete=models.SET_NULL, null=True,
                                 blank=True, db_index=True, verbose_name='категория')
    subcategory = models.ForeignKey('SubcategoriesCharacteristics', on_delete=models.SET_NULL,
                                    blank=True, null=True, verbose_name='подкатегория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Имя характеристики"
        verbose_name_plural = 'Имя характеристики'


class ValuesSpec(models.Model):
    name = models.CharField(max_length=100)
    spec = models.ForeignKey('Specifications', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Значения для характеристики"
        verbose_name_plural = "Значения для характеристики"


class CharacteristicValue(models.Model):
    name_product = models.ForeignKey('ProductSpec', related_name='product_sp',
                                     on_delete=models.SET_DEFAULT, default=0, null=True)
    name_spec = models.ForeignKey('Specifications', on_delete=models.SET_DEFAULT, default=0, null=True)
    name_value = models.ForeignKey('ValuesSpec', on_delete=models.SET_DEFAULT, default=0)
    cat = models.ForeignKey('CategoryProducts', on_delete=models.SET_DEFAULT, default=0)

    def __str__(self):
        return f'{self.name_spec} | {self.name_value}'

    class Meta:
        verbose_name = "Стек характеристик"
        verbose_name_plural = "Стек характеристик"


class ProductSpec(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('CategoryProducts', on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"


class SubcategoriesCharacteristics(models.Model):
    name = models.CharField(max_length=100, verbose_name='подкатегория')
    priority = models.SmallIntegerField(default=99, verbose_name='приоритет сортировки')
    category = models.ForeignKey('CategoryProducts', on_delete=models.SET_NULL,
                                 blank=True, null=True, verbose_name='категория')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
