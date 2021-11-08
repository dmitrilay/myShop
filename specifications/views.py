import json
import os
from django.shortcuts import render
from myshop.settings import BASE_DIR
from .models import *


def import_js(request):
    def spec_value_is_db():
        dict_1, dict_2, dict_3 = {}, {}, {}
        for y in Specifications.objects.all():
            dict_1[str(y)] = y
        for y in ValuesSpec.objects.all():
            dict_2[str(y)] = y
        for y in ProductSpec.objects.all():
            dict_3[str(y)] = y

        return dict_1, dict_2, dict_3

    dict_value_spec, dict_spec_db, dict_product_db = {}, {}, {}
    # data_js = opening_closing_file(action='r', name='spec_json.txt', type_f='json')
    data_js = opening_closing_file(action='r', name='spec.txt', type_f='json')

    dict_specifications, dict_value_spec, dict_product = spec_value_is_db()
    dict_bulk_spec, dict_bulk_value, dict_bulk_product = {}, {}, {}

    for i, i2 in data_js.items():
        name_product = i
        if not dict_product.get(name_product):  # Если нет такого значения в базе
            if not dict_bulk_product.get(name_product):  # Если нет такого значения в словаре
                dict_bulk_product[name_product] = (ProductSpec(name=name_product))

        for name_spec_js, value_spec_js in i2.items():
            if not dict_specifications.get(name_spec_js):  # Если нет такого значения в базе
                if not dict_bulk_spec.get(name_spec_js):  # Если нет такого значения в словаре
                    dict_bulk_spec[name_spec_js] = (Specifications(name=name_spec_js))
            if not dict_value_spec.get(value_spec_js):
                if not dict_bulk_value.get(value_spec_js):
                    dict_bulk_value[value_spec_js] = (ValuesSpec(name=value_spec_js))

    ProductSpec.objects.bulk_create(dict_bulk_product.values())
    Specifications.objects.bulk_create(dict_bulk_spec.values())
    ValuesSpec.objects.bulk_create(dict_bulk_value.values())
    dict_specifications, dict_value_spec, dict_product = spec_value_is_db()
    # =======================
    # Связывание таблиц db
    # =======================
    cat, obj = CategoryProducts.objects.get_or_create(name_cat='Смартфоны')
    rel = CharacteristicValue.objects.select_related('name_spec', 'name_value', 'name_product').all()

    dict_conv_db = {}
    for rel_s in rel:
        p = str(rel_s.name_product)
        t = str(rel_s.name_spec)
        v = str(rel_s.name_value)

        f = f'{p}{t}{v}'
        dict_conv_db[f] = [p, t, v]

    dict_conv_js = {}
    for rel_s, rel_s2 in data_js.items():
        p = rel_s
        for i, i2 in rel_s2.items():
            t = i
            v = i2
            f = f'{p}{t}{v}'
            dict_conv_js[f] = [p, t, v]

    list_spec_value = []
    for i in dict_conv_js:
        if dict_conv_db.get(i):
            pass
        else:
            list_spec_value.append(CharacteristicValue(name_product=dict_product[dict_conv_js[i][0]],
                                                       name_spec=dict_specifications[dict_conv_js[i][1]],
                                                       name_value=dict_value_spec[dict_conv_js[i][2]],
                                                       cat=cat))
    CharacteristicValue.objects.bulk_create(list_spec_value)

    context = {'product': 'update', 'category': 'пустота'}
    return render(request, 'base.html', context)


def opening_closing_file(data=None, name=None, action=None, type_f=None):
    name = os.path.normpath(f'{BASE_DIR}/data/{name}')
    if action == 'w':
        with open(name, 'w', encoding='utf-8') as file:
            if type_f == 'json':
                file.write(json.dumps(data))
            else:
                file.write(data.text)
    elif action == 'r':
        with open(name, 'r', encoding='utf-8') as file:
            if type_f == 'json':
                data = file.read()
                data = json.loads(data)
            else:
                data = file.read()
        return data


def priority_spec(request):
    js_dict = {}
    data_js = opening_closing_file(action='r', name='priority_spec.txt', type_f='json')

    for key, value in data_js.items():
        if not js_dict.get(key):
            js_dict[key] = [*value.keys(), *value.values()]

    spec = Specifications.objects.all()
    for i in spec:
        name_key = i.name
        if js_dict.get(name_key):
            i.participation_filtering = js_dict[name_key][0]
            i.priority_spec = js_dict[name_key][1]
    Specifications.objects.bulk_update(spec, ['participation_filtering', 'priority_spec'])
    context = {'product': 'update', 'category': 'пустота'}
    return render(request, 'base.html', context)


def delete_spec(request):
    CharacteristicValue.objects.all().delete()
    ProductSpec.objects.all().delete()
    ValuesSpec.objects.all().delete()
    Specifications.objects.all().delete()

    context = {'product': 'update', 'category': 'пустота'}
    return render(request, 'base.html', context)
