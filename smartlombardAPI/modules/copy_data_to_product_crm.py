from shop.models import Product, Category, ProductImage
from pytils.translit import slugify
import os
import uuid
from PIL import Image


def copy_data_to_product_crm_fun(instance):

    permission_validation = instance.available
    permission_write = Product.objects.filter(id_crm=instance.article).exists()

    if permission_validation == True and permission_write == False:
        cat = Category.objects.filter(name=instance.category)

        if cat.__len__() == 0:
            cat_value = instance.category
            cat = Category.objects.create(name=cat_value, slug=slugify(cat_value))
        else:
            cat = cat[0]

        Product.objects.create(condition='new',
                               category=cat,
                               name=instance.name,
                               url_spec=instance.url_spec,
                               slug=instance.slug,
                               name_spec=instance.name_spec,
                               description=instance.features,
                               price=instance.price,
                               id_crm=instance.article,
                               storage=instance.storage
                               )

        img_set = instance.productSET.all()
        for i in img_set:
            saving_photos(instance=i)


def saving_photos(**kwargs):
    obj = Product.objects.filter(name=kwargs['instance'].product)
    if len(obj) > 0:
        obj = obj[0]
        img = kwargs['instance'].image

        all_photo = kwargs['instance'].product.productSET.all()
        is_main = True if str(all_photo[0]) == str(img) else False

        img1, img2 = image_preparation(obj.category.slug, obj.slug, img)
        ProductImage.objects.create(product=obj, image=img1, imageOLD=img2, is_main=is_main,)
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


""" АРХИВ"""
# def add_photo(instance, _r):
#     data = instance.productSET.all()
#     bulk_list = []
#     for index, item in enumerate(data):
#         args = {"product": _r, "image": item.image, "is_main": True if index == 0 else False, }
#         bulk_list.append(ProductImage(**args))
#     if not bulk_list:
#         args = {"product": _r, "image": 'img_default/no_image.jpg', "is_main": True,
#                 "is_active": True, "name": 'no_fofo'}
#         ProductImage.objects.get_or_create(**args)
#     else:
#         ProductImage.objects.bulk_create(bulk_list)
