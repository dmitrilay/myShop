from unicodedata import category

from shop.models import Product
from .models import Specifications, ValuesSpec, CharacteristicValue, ProductSpec, CategoryProducts


class RecordingUniqueValues():
    def __init__(self, spec_list, value_list, product):
        self.spec_list = spec_list
        self.value_list = value_list
        self.product = product

    def spec(self):
        _sp = Specifications.objects.filter(name__in=self.spec_list).values_list('name')
        _sp = list(map(lambda x: x[0], _sp))

        not_list_spec = []

        for item in self.spec_list:
            try:
                _sp.index(str(item))
            except:
                not_list_spec.append(item)

        bulk_list = []
        for item in not_list_spec:
            bulk_list.append(Specifications(name=item))

        Specifications.objects.bulk_create(bulk_list)

    def value(self):
        _sp = ValuesSpec.objects.filter(name__in=self.value_list).values_list('name')
        _sp = list(map(lambda x: x[0], _sp))

        not_list = []

        for item in self.value_list:
            try:
                _sp.index(str(item))
            except:
                not_list.append(item)

        bulk_list = []
        for item in not_list:
            bulk_list.append(ValuesSpec(name=item))
        ValuesSpec.objects.bulk_create(bulk_list)

    def write(self):
        product = self.product.popitem()
        specifications = product[1]
        name = product[0]

        _shop_product = Product.objects.filter(name=name).values('category__name', 'id')
        if not _shop_product:
            return

        _spec_category, _ = CategoryProducts.objects.get_or_create(name_cat=_shop_product[0]['category__name'])
        _spec_product, object_exists = ProductSpec.objects.get_or_create(name=name, category=_spec_category)

        if object_exists == True:
            _sp = Specifications.objects.filter(name__in=self.spec_list)
            _vl = ValuesSpec.objects.filter(name__in=self.value_list)

            bulk_list = []
            for item in specifications:
                _s, _v = 0, 0
                for spec in _sp:
                    if spec.name == str(item[0]):
                        _s = spec
                        break
                for spec in _vl:
                    if spec.name == str(item[1]):
                        _v = spec
                        break
                bulk_list.append(CharacteristicValue(name_product=_spec_product,
                                                     name_spec=_s, name_value=_v, cat=_spec_category),)

            CharacteristicValue.objects.bulk_create(bulk_list)
            Product.objects.filter(id=_shop_product[0]['id']).update(name_spec=name)
        else:
            Product.objects.filter(id=_shop_product[0]['id']).update(name_spec=name)
