from django.db import models
from django.urls import reverse
import os
import uuid
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.core.validators import FileExtensionValidator


def image_folder(instance, filename):
    return 'photos/{}.webp'.format(uuid.uuid4().hex)


class Slider(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):
        if self.image != self.__original_image:
            name = uuid.uuid4().hex
            image1 = Image.open(self.image)
            image1.save(f'media/slider/{name}.webp', 'WEBP')

            image2 = Image.open(self.image)
            image2.save(f'media/slider/{name}.jpeg', 'jpeg', quality=80)

            self.image = f'slider/{name}.webp'
            self.imageOLD = f'slider/{name}.jpeg'
        super(Slider, self).save(*args, **kwargs)

    name = models.CharField(max_length=100, verbose_name='Имя слайда')
    image = models.ImageField(verbose_name=_('Image'), upload_to='del/',)
    imageOLD = models.ImageField(verbose_name='JPG', upload_to='del/', blank=True)
    link_transition = models.URLField(verbose_name='Ссылка для перехода', blank=True, null=True)

    class Meta:
        verbose_name = 'Фотографии для слайдера'
        verbose_name_plural = '4. Фотографии слайдера'

    def __str__(self):
        return self.name


class Category(models.Model):
    def name_file(instance, filename):
        type_file = filename.split('.')[-1]
        return f'img_category/{instance.name}/{uuid.uuid4().hex}.{type_file}'

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to=name_file,
                              verbose_name="Изображение", blank=True)

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete()

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'img_default/no_image.jpg'
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = '2. Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    MONTH_CHOICES = (
        ("new", "Новый"),
        ("used", "б/у"),
    )

    condition = models.CharField(
        choices=MONTH_CHOICES, max_length=100, db_index=True, blank=False, verbose_name='состояние')

    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    name_spec = models.CharField(max_length=200, db_index=True, blank=True)
    url_spec = models.URLField(blank=True, null=True, verbose_name='URL на карточку товара')
    uploading_csv_file = models.FileField(upload_to='uploads/', blank=True, null=True,
                                          verbose_name='Вложение с характеристиками (CSV)',
                                          validators=[FileExtensionValidator(['csv'])])
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    available = models.BooleanField(default=True, verbose_name='доступность')
    sold = models.BooleanField(default=False, verbose_name='продан')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id_crm = models.CharField(max_length=10, verbose_name='id продукта в CRM', blank=True, null=True)
    storage = models.IntegerField(default=1, verbose_name='Остатки')

    class Meta:
        ordering = ('-id',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = '1. Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.category.slug, self.slug])


class ProductImage(models.Model):
    def name_file(instance, filename):
        category = instance.product.category.slug
        name_product = instance.product.slug
        _path = f'product_photos/{category}/{name_product}/{filename}'
        return _path

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    image = models.ImageField(upload_to=name_file, verbose_name="Изображение", null=True, max_length=250)
    imageOLD = models.ImageField(upload_to=name_file, verbose_name='Изображение jpg',
                                 blank=True, null=True, max_length=250)
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")
    name = models.CharField(max_length=200, db_index=True, default=uuid.uuid4(), verbose_name="Имя")
    compression = models.BooleanField(default=False, verbose_name="Сжатие фотографии")
    # unique=True

    def __str__(self):
        return "%s" % self.pk

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = '3. Фотографии товаров'
