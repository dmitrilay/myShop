from django.core.signals import request_finished
from django.dispatch import receiver

from django.db.models.signals import post_save


from .models import ProductCRM, NewProductCRM
from shop.models import Product, Category, ProductImage
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


@receiver(post_save, sender=NewProductCRM)
def my_callback2(sender, **kwargs):
    if kwargs.get('instance'):

        permission_validation = kwargs['instance'].available
        permission_write = Product.objects.filter(id_crm=kwargs['instance'].article).exists()

        if permission_validation == True and permission_write == False:
            cat = Category.objects.filter(name=kwargs['instance'].category)

            if cat.__len__() == 0:
                cat_value = kwargs['instance'].category
                cat = Category.objects.create(name=cat_value, slug=slugify(cat_value))
            else:
                cat = cat[0]

            result = Product.objects.create(condition=kwargs['instance'].condition,
                                            category=cat,
                                            name=kwargs['instance'].name,
                                            slug=kwargs['instance'].slug,
                                            name_spec=kwargs['instance'].name_spec,
                                            description=kwargs['instance'].features,
                                            price=kwargs['instance'].price,
                                            id_crm=kwargs['instance'].article,
                                            storage=kwargs['instance'].storage
                                            )

            data = kwargs['instance'].productSET.all()
            bulk_list = []

            for index, item in enumerate(data):
                bulk_list.append(ProductImage(product=result,
                                              image=item.image,
                                              is_main=True if index == 0 else False,
                                              ))

            ProductImage.objects.bulk_create(bulk_list)
