from django.core.signals import request_finished
from django.dispatch import receiver

from django.db.models.signals import post_save
from .models import ProductCRM
from shop.models import Product, Category
from pytils.translit import slugify


@receiver(post_save, sender=ProductCRM)
def my_callback(sender, **kwargs):
    if kwargs.get('instance'):
        cat = Category.objects.filter(name=kwargs['instance'].category)

        if cat.__len__() == 0:
            cat_value = kwargs['instance'].category
            cat = Category.objects.create(name=cat_value, slug=slugify(cat_value))
            print(cat)
        else:
            cat = cat[0]

        Product.objects.create(condition=kwargs['instance'].condition,
                               category=cat,
                               name=kwargs['instance'].name,
                               slug=kwargs['instance'].slug,
                               name_spec=kwargs['instance'].name_spec,
                               description=kwargs['instance'].features,
                               price=kwargs['instance'].price,
                               available=True if kwargs['instance'].hidden == False else False,
                               id_crm=kwargs['instance'].article,
                               )
