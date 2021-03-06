from ast import Try
import datetime
from encodings import utf_8
import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from myshop.settings import BASE_DIR
import urllib.parse
from .models import *


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

    bulk_list = []
    for event in new_product:
        _event = event['data'] if event.get('data') else 0

        # print(event)

        if event['type'] == 'add':
            bulk_list.append(ProductCRM(name=_event['name'],
                                        article=_event['article'],
                                        price=_event['price'],
                                        features=_event['features'],
                                        category=_event['category'],
                                        subcategory=_event['subcategory'],
                                        hidden=_event['hidden'] if _event.get('hidden') else 0,
                                        sold=_event['sold'] if _event.get('sold') else 0,
                                        ))
            # write_file(f'{_event}', name='product_add')
            status.append({"status": True, "type": "good-add", "unique": '1', })
        elif event['type'] == 'edit':
            # write_file(f'{_event}', name='product_edit')
            status.append({"status": True, "type": "good-edit", "unique": '1', })
        elif event['type'] == 'remove':
            # _event = event['article']
            # write_file(f'{event}', name='product_remove')
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
    encodedStr = request.body.decode('utf-8')
    print('=======================')
    print(encodedStr)

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
