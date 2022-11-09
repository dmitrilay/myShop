from django.db import models
import itertools
from pytils.translit import slugify
from django.core.validators import FileExtensionValidator


class BaseProductCrmMixin(models.Model):
    MONTH_CHOICES = (
        ("new", "Новый"),
        ("used", "б/у"),
    )
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(default='', blank=True)
    name_spec = models.CharField(max_length=200, db_index=True, blank=True,
                                 verbose_name='название для поиска характеристик')
    url_spec = models.URLField(blank=True, null=True, verbose_name='URL на карточку товара')
    uploading_csv_file = models.FileField(upload_to='uploads/', blank=True, null=True,
                                          verbose_name='Вложение с характеристиками (CSV)',
                                          validators=[FileExtensionValidator(['csv'])])
    condition = models.CharField(choices=MONTH_CHOICES, default=MONTH_CHOICES[1], max_length=200,
                                 db_index=True, verbose_name='состояние')
    article = models.CharField(max_length=20, verbose_name='id продукта в CRM')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    features = models.TextField(blank=True, verbose_name='описание товара')
    category = models.CharField(max_length=200, db_index=True, verbose_name='категория')
    subcategory = models.CharField(max_length=200, verbose_name='подкатегория', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=False, verbose_name='Подтвердить модерацию')
    storage = models.IntegerField(verbose_name='Остатки', default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def _generate_slug(self):
        value = self.name
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


class ProductCRM(BaseProductCrmMixin):
    sold = models.BooleanField(default=False, null=True, verbose_name='товар является проданным')

    class Meta:
        verbose_name = "Товары из CRM"
        verbose_name_plural = "2. Б/У товары из CRM"


class NewProductCRM(BaseProductCrmMixin):
    class Meta:
        verbose_name = "Товары(NEW) из CRM"
        verbose_name_plural = "1. Новые товары из CRM"


class BaseProductCrmImageMixin(models.Model):
    image = models.ImageField(upload_to='garbage/', verbose_name="Изображение")
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")

    def __str__(self):
        return "%s" % self.image

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'
        abstract = True


class NewProductCrmImage(BaseProductCrmImageMixin):
    args = {"related_name": 'productSET', "verbose_name": "Продукт"}
    product = models.ForeignKey(NewProductCRM, blank=True, null=True, on_delete=models.CASCADE, **args)


class OldProductCrmImage(BaseProductCrmImageMixin):
    args = {"related_name": 'productSET', "verbose_name": "Продукт"}
    product = models.ForeignKey(ProductCRM,  blank=True, null=True, on_delete=models.CASCADE, **args)
