from shop.models import Product, Category, ProductImage
from pytils.translit import slugify
from django.core.files.base import ContentFile


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

        for i in instance.productSET.all():
            saving_photos(instance=i)


def saving_photos(instance):
    obj = Product.objects.filter(name=instance.product)
    if len(obj) > 0:
        new_file = ContentFile(instance.image.file.read())
        new_file.name = f"file_name.{instance.image.name.split('.')[-1]}"
        ProductImage.objects.create(product=obj[0], image=new_file, is_main=instance.is_main)
