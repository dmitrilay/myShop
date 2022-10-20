from shop.models import Product, Category
from ..models import Specifications, ValuesSpec, CharacteristicValue, ProductSpec, CategoryProducts


class RecordingUniqueValues():
    def __init__(self, spec_list, value_list, product, product_name):
        self.spec_list = spec_list
        self.value_list = value_list
        self.product = product
        self.product_name = product_name

    def spec(self):
        """Формируем список характеристик для записи в базу"""
        product_category = Category.objects.filter(products__name=self.product_name)
        product_category = product_category[0].name if product_category else 0
        spec_category, _ = CategoryProducts.objects.get_or_create(name_cat=product_category)
        _sp = Specifications.objects.filter(name__in=self.spec_list).values_list('name', 'category__name_cat')
        _sp = {x[0]: x[1] for x in _sp}

        not_list_spec = []

        for item in self.spec_list:
            if _sp.get(item):
                if _sp[item] != product_category:
                    not_list_spec.append(item)
            else:
                not_list_spec.append(item)

        bulk_list = [Specifications(name=item, category=spec_category) for item in not_list_spec]
        Specifications.objects.bulk_create(bulk_list)

    def value(self):
        """Формируем список значений для записи в базу"""
        _sp = ValuesSpec.objects.filter(name__in=self.value_list).values_list('name')
        _sp = map(lambda x: x[0], _sp)
        not_list = list(set(self.value_list) - set(_sp))
        bulk_list = [ValuesSpec(name=item) for item in not_list]
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
            _sp = Specifications.objects.filter(name__in=self.spec_list, category__name_cat=_spec_category)
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
