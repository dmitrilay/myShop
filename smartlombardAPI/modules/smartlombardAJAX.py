import datetime
import os
from myshop.settings import BASE_DIR
import urllib.parse
from django.utils.encoding import smart_str
import json
from smartlombardAPI.models import ProductCRM
from shop.models import Product


def write_file(obj, name):
    today = datetime.datetime.today()
    data = today.strftime("%Y-%m-%d-%H.%M.%S")
    _path = os.path.join(BASE_DIR, 'smartlombard', f'{name}_{data}.txt')
    with open(_path, 'w', encoding='utf-8') as f:
        f.write(obj)


def data_conversion(request):
    encodedStr = request.body.decode('utf-8')
    _print = urllib.parse.unquote_plus(encodedStr)
    _print = smart_str(_print, encoding='unicode',)
    start_crop = _print.find('[', 0)
    end_crop = _print.rfind(']', 0)+1
    _print = _print[start_crop:end_crop]
    _print = json.loads(_print)
    return _print


def type_operation(obj):
    new_product, merchants = '', ''
    data, *_ = obj

    if data.get('data'):
        if data['data'].get('goods'):
            new_product = data['data']['goods']
        if data['data'].get('merchants'):
            merchants = data['data']['merchants']

    return (new_product, merchants)


class AddingEditingProduct():
    def __init__(self, status, add_type, edit_type, remove_type) -> None:
        self.add_type = add_type
        self.edit_type = edit_type
        self.remove_type = remove_type
        self.status = status
        self.main_list_product = None
        self.crm_list_product = None
        self.index_letter = 'u'
        self.get_product()

    def add_status(self, type):
        self.status.append({"status": True, "type": type, "unique": '1', })

    def add_product(self):
        """Добавление нового товара"""
        new_product, bulk_list = self.add_type, []

        for e in new_product:
            write_permission_main, write_permission_crm = self.product_search_in_list(e['article'])

            if write_permission_main == True and write_permission_crm == True:
                bulk_list.append(ProductCRM(name=e['name'],
                                            article=f"{self.index_letter}{e['article']}",
                                            price=e['price'],
                                            features=e['features'],
                                            category=e['category'],
                                            subcategory=(e['subcategory'] if e.get('subcategory') else ''),
                                            condition='used',
                                            storage=1
                                            ))

            self.add_status("good-add")
        ProductCRM.objects.bulk_create(bulk_list)

    def edit_product(self):
        """Редактирование остатков товара"""
        new_product = self.edit_type
        for e in new_product:
            main_list_product, crm_list_product = self.product_search_in_list(e['article'])
            article, e = e['article'], e['data']
            if 'sold' in e:
                args = {'sold': True, 'storage': 0} if e['sold'] else {'sold': False, 'storage': 1}
                article = f"{self.index_letter}{article}"
                if not crm_list_product == True:
                    ProductCRM.objects.filter(article=article).update(**args)

                if not main_list_product == True:
                    Product.objects.filter(id_crm=article).update(available=False, **args)

            self.add_status("good-edit")

    def remove_product(self):
        for e in self.remove_type:
            main_list_product, crm_list_product = self.product_search_in_list(e['article'])
            article = f"{self.index_letter}{e['article']}"

            if not crm_list_product == True:
                ProductCRM.objects.filter(article=article).delete()

            if not main_list_product == True:
                Product.objects.filter(id_crm=article).update(available=False)
        self.add_status("good-remove")

    def get_product(self):
        q = Product.objects.exclude(id_crm='').values_list('id_crm')
        self.main_list_product = [x[0] for x in q]

        q = ProductCRM.objects.all().values_list('article')
        self.crm_list_product = [x[0] for x in q]

    def product_search_in_list(self, elem):
        elem = f'{self.index_letter}{elem}'
        u1 = True if not elem in self.main_list_product else False
        u2 = True if not elem in self.crm_list_product else False
        return [u1, u2]


def decomposition_data(products):
    edit_type, add_type, remove_type = [], [], []
    for product in products:
        if product['type'] == 'add':
            add_type.append(product['data'])
        elif product['type'] == 'edit':
            edit_type.append(product)
        elif product['type'] == 'remove':
            remove_type.append(product)

    return (add_type, edit_type,  remove_type)


def create_new_shop(status, merchants):
    """Добавление нового магазина"""
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
