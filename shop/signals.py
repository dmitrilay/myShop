from django.utils.translation import ugettext_lazy as _
import re
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Product, ProductImage, Category
from django.core.signals import request_finished
from specifications.utilities.Recording_сharacteristics import RecordingUniqueValues


@receiver(pre_save, sender=Category)
def photo_post_delete_handler_category(sender, instance, **kwargs):
    """Удаление фото после очистки поля в admin panel"""
    if not instance.pk:
        return False
    old_file = Category.objects.get(pk=instance.pk).image
    new_file = instance.image

    if new_file != old_file and old_file:
        if 'no_image.jpg' not in str(old_file):
            old_file.delete(save=False)


@receiver(post_delete, sender=ProductImage)
def photo_post_delete_handler(sender, instance, **kwargs):
    """Очиста фотографий после удаления в admin panel"""
    if instance.image.name:
        [x.delete() for x in [instance.imageOLD, instance.image]]
        instance.delete()


@receiver(post_save, sender=Product)
def my_callback(sender, **kwargs):
    if kwargs.get('instance'):
        if kwargs['instance'].uploading_csv_file:
            byte_content = kwargs['instance'].uploading_csv_file.open().read()
            content = byte_content.decode()
            content = clearing_css_file(content)
            write_specs(content, kwargs['instance'])
            # kwargs['instance'].uploading_csv_file.delete()


def write_specs(content, props):
    """Запись характеристик из css файла"""
    list_spec = [[x.split(';')[0], x.split(';')[1]] for x in content if x]
    d = dict(list_spec)
    _keys, _values = list(d.keys()), list(d.values())
    product_and_spec = {props.name: list_spec, }
    _ = {'spec_list': _keys, 'value_list': _values, 'product': product_and_spec, 'product_name': props.name}
    obj = RecordingUniqueValues(**_)

    obj.spec()
    obj.value()
    obj.write()


def clearing_css_file(content):
    """Удаление дублированых ковычек полученых из csv файла"""
    content = content.replace('\ufeff', '')
    pattern = r'["]{2,5}[\d\w]{1,20}["]{2,5}'

    while re.search(pattern, content):
        search_elem = re.search(pattern, content)
        new_elem = re.findall(r'[^"]{1,6}', search_elem[0])
        new_elem = f'"{new_elem[0]}"' if new_elem else ''
        start, end = search_elem.span()
        content = f'{content[:start]}{new_elem}{content[end:]}'

    pattern = r'"[\d\w.\.]{1,20}["]{3}'
    while re.search(pattern, content):
        search_elem = re.search(pattern, content)
        new_elem = re.findall(r'[\d\w\.]{1,20}"', search_elem[0])
        start, end = search_elem.span()
        content = f'{content[:start]}{new_elem[0]}{content[end:]}'

    return content.split('\r\n')
