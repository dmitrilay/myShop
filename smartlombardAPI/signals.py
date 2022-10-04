from django.core.signals import request_finished
from django.dispatch import receiver

from django.db.models.signals import post_save, pre_save


from .models import ProductCRM, NewProductCRM, NewProductCrmImage
from shop.models import Product, Category, ProductImage
from pytils.translit import slugify

import os
import uuid
from PIL import Image


@receiver(post_save, sender=ProductCRM)
def my_callback(sender, **kwargs):

    if kwargs.get('instance'):

        permission_validation = kwargs['instance'].available
        permission_write = Product.objects.filter(id_crm=kwargs['instance'].article).exists()

        if permission_validation == True and permission_write == False:
            cat = Category.objects.filter(name=kwargs['instance'].category)

            if cat.__len__() == 0:
                cat_value = kwargs['instance'].category
                cat = Category.objects.create(name=cat_value, slug=slugify(cat_value))
                print(cat)
            else:
                cat = cat[0]

            _r = Product.objects.create(condition=kwargs['instance'].condition,
                                        category=cat,
                                        name=kwargs['instance'].name,
                                        slug=kwargs['instance'].slug,
                                        name_spec=kwargs['instance'].name_spec,
                                        url_spec=kwargs['instance'].url_spec,
                                        description=kwargs['instance'].features,
                                        #    price=kwargs['instance'].price,
                                        price='99999',
                                        available=True if kwargs['instance'].hidden == False else False,
                                        sold=True if kwargs['instance'].sold == True else False,
                                        id_crm=kwargs['instance'].article,
                                        )
            add_photo(kwargs, _r)


@receiver(post_save, sender=NewProductCrmImage)
def callback_saving_photos(sender, **kwargs):
    saving_photos(**kwargs)


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

            Product.objects.create(condition=kwargs['instance'].condition,
                                   category=cat,
                                   name=kwargs['instance'].name,
                                   url_spec=kwargs['instance'].url_spec,
                                   slug=kwargs['instance'].slug,
                                   name_spec=kwargs['instance'].name_spec,
                                   description=kwargs['instance'].features,
                                   price=kwargs['instance'].price,
                                   id_crm=kwargs['instance'].article,
                                   storage=kwargs['instance'].storage
                                   )

            img_set = kwargs['instance'].productSET.all()
            for i in img_set:
                saving_photos(instance=i)


def saving_photos(**kwargs):
    obj = Product.objects.filter(name=kwargs['instance'].product)
    if len(obj) > 0:
        obj = obj[0]
        img = kwargs['instance'].image
        img1, img2 = image_preparation(obj.category.slug, obj.slug, img)
        ProductImage.objects.create(product=obj, image=img1, imageOLD=img2, is_main=True,)
        Removing_photo_gags(obj)


def Removing_photo_gags(obj):
    """Удаление временной фотографии"""
    _r = ProductImage.objects.filter(product=obj)
    for item in _r:
        if item.imageOLD == 'img_default/no_image.jpg' and len(_r) > 1:
            item.delete()


def image_preparation(cat, name, image):
    """Конвертируем изображения в jpg и webp"""
    _PATH = f'media/product_photos/{cat}/{name}'
    if not os.path.exists(_PATH):
        os.makedirs(_PATH)

    name_uuid = uuid.uuid4().hex
    _PATH = f'product_photos/{cat}/{name}/{name_uuid}'

    image1 = Image.open(image)
    image1.save(f'media/{_PATH}.webp', 'WEBP')

    image2 = Image.open(image)
    image2.save(f'media/{_PATH}.jpeg', 'jpeg', quality=80)

    return [f'{_PATH}.webp', f'{_PATH}.jpeg']


def add_photo(kwargs, _r):
    data = kwargs['instance'].productSET.all()
    bulk_list = []
    for index, item in enumerate(data):
        bulk_list.append(ProductImage(product=_r, image=item.image,
                                      is_main=True if index == 0 else False,
                                      ))

    if not bulk_list:
        ProductImage.objects.get_or_create(product=_r,
                                           image='img_default/no_image.jpg',
                                           is_main=True,
                                           is_active=True,
                                           name='no_fofo')
    else:
        ProductImage.objects.bulk_create(bulk_list)
