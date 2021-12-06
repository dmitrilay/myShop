from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    # image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    name_spec = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    features = models.ManyToManyField("specs.ProductFeatures", blank=True, related_name='features_for_product')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.category.slug, self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True,
                                null=True, default=None, on_delete=models.CASCADE, verbose_name="Продукт")
    image = models.ImageField(upload_to='products_images/', verbose_name="Изображение")
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")
    is_active = models.BooleanField(default=True, verbose_name="Показывать изображение")
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    name = models.CharField(max_length=200, db_index=True, default=1, verbose_name="Имя")

    def __str__(self):
        return "%s" % self.pk

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'
