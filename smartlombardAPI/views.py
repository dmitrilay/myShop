import datetime
from itertools import product
import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from myshop.settings import BASE_DIR
import urllib.parse

from shop.models import Product
from .models import *

from django.db import connection


@csrf_exempt
def smartlombardAJAX(request):

    def write_file(obj, name):
        today = datetime.datetime.today()
        data = today.strftime("%Y-%m-%d-%H.%M.%S")
        _path = os.path.join(BASE_DIR, 'smartlombard', f'{name}_{data}.txt')
        with open(_path, 'w', encoding='utf-8') as f:
            f.write(obj)

    write_file(f'{request.body}', 'body')

    encodedStr = request.body.decode('utf-8')
    _print = urllib.parse.unquote_plus(encodedStr)
    _print = smart_str(_print, encoding='unicode',)
    start_crop = _print.find('[', 0)
    end_crop = _print.rfind(']', 0)+1
    _print = _print[start_crop:end_crop]
    _print = json.loads(_print)

    new_product, merchants = '', ''
    if _print[0].get('data'):
        if _print[0]['data'].get('goods'):
            new_product = _print[0]['data']['goods']
        if _print[0]['data'].get('merchants'):
            merchants = _print[0]['data']['merchants']

    status = []

    # Добавление нового товара
    article_in_database_main = Product.objects.filter(id_crm__gte=0).values_list('id_crm')
    article_in_database_main = list(map(lambda _i: _i[0], article_in_database_main))

    article_in_database = ProductCRM.objects.all().values_list('article')
    article_in_database = list(map(lambda _i: _i[0], article_in_database))

    bulk_list = []
    for event in new_product:
        _event = event['data'] if event.get('data') else 0

        search_product_1 = True if int(_event['article']) in article_in_database_main else False
        search_product_2 = True if int(_event['article']) in article_in_database else False

        if event['type'] == 'add':
            if search_product_1 == False and search_product_2 == False:
                bulk_list.append(ProductCRM(name=_event['name'],
                                            article=_event['article'],
                                            price=_event['price'],
                                            features=_event['features'],
                                            category=_event['category'],
                                            subcategory=_event['subcategory'],
                                            hidden=_event['hidden'] if _event.get('hidden') else 0,
                                            sold=_event['sold'] if _event.get('sold') else 0,
                                            condition='used'
                                            ))

            status.append({"status": True, "type": "good-add", "unique": '1', })
        elif event['type'] == 'edit':

            print(event['data'])

            if search_product_2 == True:
                if _event['sold'] == True:
                    ProductCRM.objects.filter(article=_event['article']).update(sold=True, hidden=True)
                elif _event['sold'] == False:
                    ProductCRM.objects.filter(article=_event['article']).update(sold=False, hidden=False)

            if search_product_1 == True:
                if _event['sold'] == True:
                    Product.objects.filter(id_crm=_event['article']).update(available=False, sold=True, storage=0)
                elif _event['sold'] == False:
                    Product.objects.filter(id_crm=_event['article']).update(available=False, sold=False, storage=1)

            status.append({"status": True, "type": "good-edit", "unique": '1', })
        elif event['type'] == 'remove':
            status.append({"status": True, "type": "good-remove", "unique": '1', })

    ProductCRM.objects.bulk_create(bulk_list)

    # Добавление нового магазина
    for event in merchants:
        _event = event['data'] if event.get('data') else 0

        if event['type'] == 'add':
            write_file(f'{_event}', name='merchant_add')
            status.append({"status": True, "type": "merchant-add", "unique": '1', })
        elif event['type'] == 'edit':
            write_file(f'{_event}', name='merchant_edit')
            status.append({"status": True, "type": "merchant-edit", "unique": '1', })
        elif event['type'] == 'remove':
            write_file(f'{event}', name='merchant_remove')
            status.append({"status": True, "type": "merchant-remove", "unique": '1', })

    # print(status)
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


# @csrf_exempt
# def smartlombardAJAX(request):

#     _p = request.method
#     # print(str(_p))
#     # print(request.method)
#     # print(request.POST)

#     # _p = request.body.decode()
#     # _p = json.loads(_p)
#     # _p = json.loads(request.body.decode())

#     # body_unicode = request.body.decode('utf-8')
#     # _p = json.loads(body_unicode)

#     # print(body_unicode)

#     def write_file(obj):
#         # today = datetime.datetime.today()
#         # data = today.strftime("%Y-%m-%d-%H.%M.%S")
#         # encoding='utf-8'
#         _path = os.path.join(BASE_DIR, 'smartlombard', 'test.txt')
#         with open(_path, 'w') as f:
#             f.write(obj)

#     write_file(f'{_p}')

#     # write_file('test')

#     _r = {
#         "status": 'true',
#         "type": "good-add",
#         "unique": 'null',
#         "message": "Необязательное поле"
#     }

#     return JsonResponse(_r)


# def SearchProductAjax(request):
#     product_name = request.GET.get('search')

#     product_list = []
#     if product_name:
#         rez = Product.objects.filter(name__icontains=product_name)[:10]
#         for item in rez:
#             product_list.append({'name': item.name, 'url': item.get_absolute_url()})

#     return JsonResponse({"product_list": product_list})
