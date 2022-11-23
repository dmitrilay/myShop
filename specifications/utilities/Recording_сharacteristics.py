import re
from unicodedata import name
from shop.models import Product, Category
from ..models import Specifications, ValuesSpec, CharacteristicValue, ProductSpec, CategoryProducts


class RecordingUniqueValues():
    def __init__(self, spec_list, value_list, product, product_name):
        self.spec_list = []
        self.value_list = []
        self.product_name = ''
        self.product = self.cyrillic_lowercase(product)

        self.splitting_array()

    def splitting_array(self):
        _d = self.product.copy()
        product = _d.popitem()

        self.product_name = product[0]
        for item in product[1]:
            self.spec_list.append(item[0])
            self.value_list.append(item[1])

    def spec(self):
        """Формируем список характеристик для записи в базу"""
        product_category = Category.objects.filter(products__name=self.product_name)
        product_category = product_category[0].name if product_category else 0
        spec_category, _ = CategoryProducts.objects.get_or_create(name_cat=product_category)

        _params = {"name__in": self.spec_list, "category__name_cat": spec_category.name_cat}
        _sp = Specifications.objects.filter(**_params).values_list('name', )
        _sp = [x[0] for x in _sp]

        not_list_spec = []

        for item in self.spec_list:
            if not item in _sp:
                not_list_spec.append(item)

        bulk_list = [Specifications(name=item, category=spec_category) for item in not_list_spec]
        Specifications.objects.bulk_create(bulk_list)

    def value(self):
        """Формируем список значений для записи в базу"""
        _sp = ValuesSpec.objects.filter(name__in=self.value_list).values_list('name')
        _sp = [x[0] for x in _sp]

        not_list = list(set(self.value_list) - set(_sp))
        bulk_list = [ValuesSpec(name=item) for item in not_list]
        ValuesSpec.objects.bulk_create(bulk_list)

    def write(self):
        """Создаем или обновляем стек характеристик"""
        product = self.product.popitem()
        specifications = product[1]
        name = product[0]

        _shop_product = Product.objects.filter(name=name).values('category__name', 'id', 'name_spec')
        if not _shop_product:
            return

        _spec_category, _ = CategoryProducts.objects.get_or_create(name_cat=_shop_product[0]['category__name'])
        _spec_product, _ = ProductSpec.objects.get_or_create(name=name, category=_spec_category)

        _sp = Specifications.objects.filter(name__in=self.spec_list, category__name_cat=_spec_category)
        _vl = ValuesSpec.objects.filter(name__in=self.value_list)
        stack_of_characteristics = CharacteristicValue.objects.filter(
            name_product__name=name).values_list('name_spec__name',)
        stack_of_characteristics = [x[0] for x in stack_of_characteristics]

        bulk_list = []
        list_stack_spec = []
        for item in specifications:
            _spec, _value = item
            if _spec not in stack_of_characteristics:
                list_stack_spec.append([_spec, _value])

        list_stack_spec = self.get_object_by_name(list_stack_spec, _sp, 'spec')
        list_stack_spec = self.get_object_by_name(list_stack_spec, _vl, 'value')

        for item in list_stack_spec:
            _spec, _value = item
            _args = {'name_product': _spec_product, 'name_spec': _spec, 'name_value': _value, 'cat': _spec_category}
            bulk_list.append(CharacteristicValue(**_args))

        CharacteristicValue.objects.bulk_create(bulk_list)

        if _spec_product and _shop_product[0]['name_spec'] == '':
            Product.objects.filter(id=_shop_product[0]['id']).update(name_spec=name)

    @staticmethod
    def get_object_by_name(list_stack_spec, objs, spec_or_value):
        """Поиск значений в списке и замена найденного на объекты"""
        _index = 0 if spec_or_value == 'spec' else 1
        for i in range(len(list_stack_spec)):
            item = str(list_stack_spec[i][_index])
            for obj in objs:
                if obj.name == item:
                    list_stack_spec[i][_index] = obj
                    break
        return list_stack_spec

    @staticmethod
    def cyrillic_lowercase(obj):
        """Всю кириллицу конвертируем в нижний регистр, кроме первой буквы. А так же приводим к строке"""
        def convert(text):
            if re.search(r'[a-я]', str(text)):
                text_lower = text.lower()
                text = text_lower[:1].upper() + text_lower[1:]
            else:
                text = str(text)
            return text

        product = obj.popitem()
        product_name = product[0]

        obj = {product_name: []}
        for item in product[1]:
            obj[product_name].append([item[0], convert(item[1])])

        return obj
