from itertools import product
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
from shop.models import Product
from .models import *
from django.db import connection
from .modules.smartlombardAJAX import *


@csrf_exempt
def smartlombardAJAX(request):
    write_file(f'{request.body}', 'body')
    data = data_conversion(request)
    new_product, merchants = type_operation(data)
    status = []
    add_type, edit_type, remove_type = decomposition_data(new_product)
    p = AddingEditingProduct(status, add_type, edit_type, remove_type)
    p.add_product()
    p.edit_product()
    create_new_shop(status, merchants)

    return JsonResponse(status, safe=False)


@csrf_exempt
def v2smartlombardAJAX(request):
    data = request.body.decode('utf-8')
    data = data[5:]
    data = urllib.parse.unquote_plus(data)
    data = json.loads(data)

    bulk_create_list = []
    bulk_update_list = []
    result = [f'n{x}' for x in data]

    """Проверяем товары в основном списке, если они там есть - обновляем остатки"""
    product = Product.objects.filter(id_crm__in=result).values_list('id_crm', 'storage')

    product = {str(x[0]): x[1] for x in product}
    list_del = []
    for key, item in data.items():
        key = f'n{key}'
        if product.get(key) != None:
            storage = product[key] + item[1] if product[key] + item[1] > 0 else 0
            _r = Product.objects.get(id_crm=key)
            _r.storage = storage
            _r.available = True if product[key] + item[1] > 0 else False
            bulk_update_list.append(_r)
            list_del.append(key[1:])

    Product.objects.bulk_update(bulk_update_list, ["storage", 'available'])
    # удаляем элемент из словоря
    _ = [data.pop(i) for i in list_del]

    """Добовляем товар для модерации, отрицательные остатки не допустимы!"""
    new_product_crm = NewProductCRM.objects.filter(article__in=result).values_list('article', 'storage')
    new_product_crm = {str(x[0]): x[1] for x in new_product_crm}

    for key, item in data.items():
        q_article = f'n{key}'
        q_name, q_storage, q_price, q_category, q_subcategory = item[0], item[1], item[2], item[3], item[4]

        if new_product_crm.get(q_article) != None:
            storage = new_product_crm[q_article] + q_storage
            storage = 0 if storage < 0 else storage

            _r = NewProductCRM.objects.get(article=q_article)
            _r.storage = storage
            bulk_update_list.append(_r)

        elif q_storage > 0:
            # Проверяем на отрицательные остатки
            bulk_create_list.append(NewProductCRM(name=q_name,
                                                  storage=q_storage,
                                                  price=q_price,
                                                  category=q_category,
                                                  subcategory=q_subcategory,
                                                  article=q_article,
                                                  ))

    NewProductCRM.objects.bulk_create(bulk_create_list)
    NewProductCRM.objects.bulk_update(bulk_update_list, ["storage", ])

    # print('Кол-во запросов', len(connection.queries))
    status = {"status": 200}
    return JsonResponse(status, safe=False)
