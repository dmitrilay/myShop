from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import ProductCRM, NewProductCRM, NewProductCrmImage, OldProductCrmImage

from django.core.signals import request_finished
from .modules.copy_data_to_product_crm import *
from .modules.uploading_csv_file import *

# from specifications.models import Specifications, CharacteristicValue
# from django.db.models import Count


@receiver(post_save, sender=ProductCRM)
def my_callback(sender, **kwargs):
    pass


@receiver(post_save, sender=NewProductCRM)
@receiver(post_save, sender=ProductCRM)
def callback_product_crm(sender, instance, **kwargs):
    # clean_spec()

    if instance:
        copy_data_to_product_crm_fun(instance)
    if instance.uploading_csv_file and instance.available:
        uploading_csv_file(instance)


@receiver(post_save, sender=NewProductCrmImage)
@receiver(post_save, sender=OldProductCrmImage)
def callback_saving_photos2(sender, instance, **kwargs):
    saving_photos(instance)


# def clean_spec():
#     r = Specifications.objects.annotate(count_field=Count('characteristicvalue')).filter(count_field=0)
#     r.delete()
#     # print(len(r))
