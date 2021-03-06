from tabnanny import verbose
from django.db import models
import itertools
# from django.utils.text import slugify
from pytils.translit import slugify


class ProductCRM(models.Model):
    MONTH_CHOICES = (
        ("new", "Новый"),
        ("used", "б/у"),
    )

    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(default='', blank=True)
    name_spec = models.CharField(max_length=200, db_index=True, blank=True,
                                 verbose_name='название для поиска характеристик')
    condition = models.CharField(choices=MONTH_CHOICES, max_length=200,
                                 db_index=True, verbose_name='состояние', blank=True)
    article = models.IntegerField(verbose_name='id продукта в CRM')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    features = models.TextField(blank=True, verbose_name='описание товара')
    category = models.CharField(max_length=200, db_index=True, verbose_name='категория')
    subcategory = models.CharField(max_length=200, db_index=True, verbose_name='подкатегория')
    hidden = models.BooleanField(default=False, null=True, verbose_name='скрыть товар')
    sold = models.BooleanField(default=False, null=True, verbose_name='товар является проданным')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=False, verbose_name='Подтвердить модерацию')

    class Meta:
        verbose_name = "Товары из CRM"
        verbose_name_plural = "Товары из CRM"

    def __str__(self):
        return self.name

    def _generate_slug(self):
        # max_length = self._meta.get_field('slug').max_length
        value = self.name
        # slug_candidate = slug_original = slugify(value, allow_unicode=False)
        slug_candidate = slug_original = slugify(value)
        for i in itertools.count(1):
            if not ProductCRM.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        elif self.slug == '':
            self._generate_slug()

        super().save(*args, **kwargs)


class NewProductCRM(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(default='', blank=True)
    name_spec = models.CharField(max_length=200, db_index=True, blank=True,
                                 verbose_name='название для поиска характеристик')
    condition = models.CharField(default='new', max_length=200,
                                 db_index=True, verbose_name='состояние', blank=True)
    article = models.IntegerField(verbose_name='id продукта в CRM')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    features = models.TextField(blank=True, verbose_name='описание товара')
    category = models.CharField(max_length=200, db_index=True, verbose_name='категория')
    subcategory = models.CharField(max_length=200, db_index=True, verbose_name='подкатегория', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=False, verbose_name='Подтвердить модерацию')
    storage = models.IntegerField(verbose_name='Остатки')

    class Meta:
        verbose_name = "Товары из CRM"
        verbose_name_plural = "Товары из CRM"

    def __str__(self):
        return self.name

    def _generate_slug(self):
        # max_length = self._meta.get_field('slug').max_length
        value = self.name
        # slug_candidate = slug_original = slugify(value, allow_unicode=False)
        slug_candidate = slug_original = slugify(value)
        for i in itertools.count(1):
            if not ProductCRM.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        elif self.slug == '':
            self._generate_slug()

        super().save(*args, **kwargs)
