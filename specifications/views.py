from django.utils.decorators import method_decorator
import json
import os
from collections import defaultdict
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, ListView

from myshop.settings import BASE_DIR, TOKEN_SPEC, DEBUG
from shop.models import Category, Product
from .forms import NewCategoryFeatureKeyForm
from .models import *
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

import urllib.parse
from .utilities.Recording_сharacteristics import RecordingUniqueValues

from smartlombardAPI.models import NewProductCRM, ProductCRM


# -------------------------------------------
# Создание значения для характеристики
# -------------------------------------------
class CreateNewCharacteristic(View):

    @staticmethod
    def get(request):
        categories = Product.objects.filter(name_spec='', available=True)
        context = {'categories': categories}
        return render(request, 'specs/NewTemplate/CreateNewCharacteristic.html', context)

    @staticmethod
    def post(request):
        data = request.body.decode('utf-8')
        data = json.loads(data)

        product = Product.objects.filter(pk=data['product_id']).values_list('category__name', 'name')
        obj, created = CategoryProducts.objects.get_or_create(name_cat=product[0][0])
        name_product, _ = ProductSpec.objects.get_or_create(name=product[0][1], category=obj)
        list_product_spec = CharacteristicValue.objects.filter(name_product=name_product)

        bulk_list = []
        if obj:
            for key, value in data['spec'].items():

                spec, _ = Specifications.objects.get_or_create(name=key)
                sp_value, _ = ValuesSpec.objects.get_or_create(name=value)

                _s = CharacteristicValue(name_product=name_product,
                                         name_spec=spec,
                                         name_value=sp_value,
                                         cat=obj
                                         )

                write_permission = True
                for item in list_product_spec:
                    if str(item) == str(_s):
                        write_permission = False
                        break

                bulk_list.append(_s) if write_permission else _

            print(bulk_list)
            CharacteristicValue.objects.bulk_create(bulk_list)

        return JsonResponse({"OK": "OK"})


# -------------------------------------------
# Редактирование подкатегорий
# -------------------------------------------


def forms_subcategories(request):
    priority_f = request.GET.get('priority_f')
    subcategories_f = request.GET.get('subcategories_f')
    spec_id_f = request.GET.get('spec_id_f')
    category_f = request.GET.get('category_f')
    del_f = request.GET.get('del_f')

    print(del_f)
    if del_f:
        CharacteristicValue.objects.filter(name_spec=spec_id_f).delete()
        Specifications.objects.filter(pk=spec_id_f).delete()

    if subcategories_f != '---':
        spec = Specifications.objects.get(pk=spec_id_f)
        sub_cat = SubcategoriesCharacteristics.objects.get(pk=subcategories_f)
        if sub_cat:
            spec.subcategory = sub_cat
            spec.save()

    return_path = request.META.get('HTTP_REFERER', '/')

    return redirect(return_path, permanent=True)


class EditingSubcategory(ListView):
    template_name = 'specs/editing_subcategory.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = CategoryProducts.objects.all()
        return categories


class EditingSubcategory2(ListView):
    template_name = 'specs/editing_subcategory2.html'
    context_object_name = 'Characteristics'

    def get_context_data(self, **kwargs):
        cat = self.request.GET.get('category-validators')
        context = super().get_context_data(**kwargs)
        context['list_subcategories'] = SubcategoriesCharacteristics.objects.filter(category=cat)
        context['category'] = cat
        return context

    def get_queryset(self):
        cat = self.request.GET.get('category-validators')
        categories = CharacteristicValue.objects.filter(cat=cat).values(
            'name_spec__name', 'name_spec__id', 'name_spec__subcategory__name', 'name_spec__subcategory__priority').distinct()

        _spec = list(categories)
        for item in _spec:
            if item['name_spec__subcategory__priority'] == None:
                item['name_spec__subcategory__priority'] = 1000

        _spec = sorted(_spec, key=lambda student: student['name_spec__subcategory__priority'])
        return _spec


class AllSpecView(View):
    @staticmethod
    def get(request):
        if request.user.is_superuser:
            categories = CategoryProducts.objects.all()
            context = {'categories': categories}
            return render(request, 'specs/new_product_feature.html', context)
        else:
            return redirect('login')

# -------------------------------------------
# Создание характеристик для ТОВАРА
# -------------------------------------------


class NewProductFeatureView(View):
    """Присвоение характеристики определенному товару"""

    @staticmethod
    def get(request):
        categories = CategoryProducts.objects.all()
        print(categories)
        context = {'categories': categories}
        return render(request, 'specs/new_product_feature.html', context)


class CreateNewProductFeatureAjaxView(View):
    """Создаем характеристику для товара"""

    @staticmethod
    def get(request):
        print('11111111111111')
        product = Product.objects.get(name=request.GET.get('product'))
        feature_name = request.GET.get('category_feature')
        value = request.GET.get('value')
        category_feature = CategoryProducts.objects.get(category=product.category, feature_name=feature_name)
        feature = Specifications.objects.create(feature=category_feature, product=product, value=value)
        product.features.add(feature)
        return JsonResponse({"OK": "OK"})


# -------------------------------------------
# Импорт характеристик
# -------------------------------------------
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
    data_json = opening_closing_file(action='r', name='spec.txt', type_f='json')

    dict_specifications, dict_value_spec, dict_product = spec_value_is_db()
    dict_bulk_spec, dict_bulk_value, dict_bulk_product = {}, {}, {}

    for name_product, i2 in data_json.items():
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
    for rel_s, rel_s2 in data_json.items():
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


# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------
# -------------------------------------

# -------------------------------------------
# Главная страница
# -------------------------------------------
class BaseSpecView(TemplateView):
    template_name = 'specs/base.html'


# -------------------------------------------
# Создание новой характеристики
# -------------------------------------------
# class CreateNewFeature(FormView):
#     template_name = 'specs/new_feature.html'
#     form_class = NewCategoryFeatureKeyForm
#     context_object_name = 'form'
#     success_url = '/spec/'

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


# -------------------------------------------
# Создание новой характеристики
# -------------------------------------------

class CreateFeatureView(View):
    """Создание значения для характеристики 2"""

    @staticmethod
    def get(request):
        print(request.GET)
        # category_id = request.GET.get('category_id')
        # feature_name = request.GET.get('feature_name')
        # value = request.GET.get('feature_value').strip(" ")
        # category = Category.objects.get(id=int(category_id))
        # feature = CategoryProducts.objects.get(category=category, feature_name=feature_name)
        # existed_object, created = FeatureValidator.objects.get_or_create(
        #     category=category,
        #     feature_key=feature,
        #     valid_feature_value=value
        # )

        # if not created:
        #     return JsonResponse({
        #         "error": f"Значение '{value}' уже существует."
        #     })
        # messages.add_message(
        #     request, messages.SUCCESS,
        #     f'Значение "{value}" для характеристики '
        #     f'"{feature.feature_name}" в категории {category.name} успешно создано'
        # )
        return JsonResponse({'result': 'ok'})


# -------------------------------------------
# Создание характеристик для ТОВАРА
# -------------------------------------------
# class NewProductFeatureView(View):
#     """Присвоение характеристики определенному товару"""
#
#     @staticmethod
#     def get(request):
#         categories = Category.objects.all()
#         context = {'categories': categories}
#         return render(request, 'specs/new_product_feature.html', context)


class AttachNewFeatureToProduct(View):
    """Выгружаем доступные характеристики для заданного товара"""

    @staticmethod
    def get(request):
        product_id = Product.objects.get(id=int(request.GET.get('product_id')))
        existing_features = list(set([item.feature.feature_name for item in product_id.features.all()]))
        print(existing_features)
        category_features = CategoryProducts.objects.filter(
            category=product_id.category).exclude(
            feature_name__in=existing_features)

        dict_result = dict()
        for item in category_features:
            dict_result[item.id] = [item.category.id, item.feature_name]
        json_string = json.dumps(dict_result)
        return JsonResponse({"features": json_string})


class ProductFeatureChoicesAjaxView(View):
    """Выгружаем доступные значения для характеристики"""

    @staticmethod
    def get(request):
        category = Category.objects.get(id=int(request.GET.get('category_id')))
        # feature_name = request.GET.get('product_feature_name')
        # feature_key = CategoryProducts.objects.get(category=category, feature_name=feature_name)
        # validators_qs = FeatureValidator.objects.filter(category=category, feature_key=feature_key)
        #
        # dict_result = dict()
        # for item in validators_qs:
        #     dict_result[item.id] = [item.id, item.valid_feature_value]
        #
        # json_string = json.dumps(dict_result)
        # return JsonResponse({"features": json_string})


# -------------------------------------------
# Унивирсальные классы
# -------------------------------------------


class FeatureChoiceView(View):
    """Выгружает характеристики для определенной категории"""

    @staticmethod
    def get(request):
        сat_id = request.GET.get('category_id')
        # select_related(*pf)
        pf = ('name',)
        # f = CharacteristicValue.objects.filter(cat__id=сat_id).select_related(*pf)
        f = Specifications.objects.filter(characteristicvalue__cat__id='1').distinct()

        # f3 = Specifications.objects.get(pk=100)
        # print(f3)
        # f2 = ValuesSpec.objects.filter(characteristicvalue__name_spec__id='100').distinct()
        # for i2423 in f2:
        #     print(i2423)
        #
        print('---------------')
        print('---------------')
        print('---------------')
        print('---------------')
        print('---------------')
        result_dict = dict()
        for item in f:
            result_dict[item.name] = item.name
        # print(result_dict)
        return JsonResponse({"result": result_dict})


# -------------------------------------------
# Остальное
# -------------------------------------------
# class UpdateProductFeaturesView(View):
#     @staticmethod
#     def get(request):
#         pass
#         # categories = Category.objects.all()
#         # context = {'categories': categories}
#         # return render(request, 'update_product_features.html', context)


class UpdateProductFeaturesAjaxView(View):
    @staticmethod
    def post(request):
        # pass
        features_names = request.POST.getlist('features_names')
        features_current_values = request.POST.getlist('features_current_values')
        new_feature_values = request.POST.getlist('new_feature_values')
        data_for_update = [{'feature_name': name, 'current_value': curr_val, 'new_value': new_val} for
                           name, curr_val, new_val
                           in zip(features_names, features_current_values, new_feature_values)]
        product = Product.objects.get(title=request.POST.get('product'))
        for item in product.features.all():
            for item_for_update in data_for_update:
                if item.feature.feature_name == item_for_update['feature_name']:
                    if item.value != item_for_update['new_value'] and item_for_update['new_value'] != '---':
                        cf = CategoryProducts.objects.get(
                            category=product.category,
                            feature_name=item_for_update['feature_name']
                        )
                        item.value = Specifications.objects.get(
                            category=product.category,
                            feature_key=cf,
                            valid_feature_value=item_for_update['new_value']
                        ).valid_feature_value
                        item.save()
        messages.add_message(
            request, messages.SUCCESS,
            f'Значения характеристик для товара {product.name} успешно обновлены'
        )
        return JsonResponse({"result": "ok"})


# -------------------------------------------
# Редактирование характеристик для товара
# -------------------------------------------
class UpdateProductFeaturesView(View):
    @staticmethod
    def get(request):
        categories = CategoryProducts.objects.all()
        context = {'categories': categories}
        return render(request, 'specs/update_product_features.html', context)


class SearchProductAjaxView(View):
    """Динамический поиск товара по имени"""

    @staticmethod
    def get(request):
        query = request.GET.get('query')
        if len(query) > 2:
            category_id = request.GET.get('category_id')
            category = CategoryProducts.objects.get(id=int(category_id))
            products = list(ProductSpec.objects.filter(category=category, name__icontains=query).values())
        else:
            products = ''
        return JsonResponse({"result": products})


class ShowProductFeaturesForUpdate(View):
    @staticmethod
    def get(request):
        read_get = (request.GET.get('purpose'))
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!')
        # print(read_get)
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!')
        if read_get == '1':  # выгрузка всех характеристик по значению
            value_id = (request.GET.get('value_id'))
            pf = ('name_product', 'name_spec', 'name_value')
            features = CharacteristicValue.objects.filter(id=value_id).select_related(*pf)
            f = features[0].name_spec
            data = str(f) + ' // ' + str(features[0].name_value)
            all_features = ValuesSpec.objects.filter(characteristicvalue__name_spec=f).distinct()

            select_different_values_dict = []
            for i in all_features:
                select_different_values_dict.append(str(i))
            # debug_qur()
            return JsonResponse({"result": [select_different_values_dict, data]})
        elif read_get == '2':
            value_old_id = (request.GET.get('value_id'))
            new_value_name = (request.GET.get('new_value_name'))

            if new_value_name != '---':
                features = CharacteristicValue.objects.get(id=value_old_id)
                z = ValuesSpec.objects.get(name=new_value_name)
                features.name_value = z
                features.save()

            return JsonResponse({"result": 1})

        elif read_get == '3':
            value_old_id = (request.GET.get('value_id'))
            cat_id = ProductSpec.objects.get(id=value_old_id).category.id
            p = ('id', 'name')
            all_spec = Specifications.objects.filter(characteristicvalue__cat=cat_id).distinct().values(*p)
            p = ('id', 'name')
            product_spec = Specifications.objects.filter(characteristicvalue__name_product=value_old_id).values(*p)

            all_spec_dict = {}
            for i in all_spec:
                all_spec_dict[i['id']] = i['name']

            for i in product_spec:
                all_spec_dict.pop(i['id'])

            return JsonResponse({"result": all_spec_dict})
        elif read_get == '4':
            value_id = (request.GET.get('value_id'))
            v = ('id', 'name')
            q = ValuesSpec.objects.filter(characteristicvalue__name_spec=value_id).distinct().values(*v)

            all_spec_dict = {}
            for i in q:
                all_spec_dict[i['id']] = i['name']

            return JsonResponse({"result": all_spec_dict})
        elif read_get == '5':
            """Добавление характеристики и значения для продукта"""
            # TODO: необходимо добавить правильную категорию
            name_characteristic = (request.GET.get('name_characteristic'))
            name_value = (request.GET.get('name_value'))
            product = (request.GET.get('product'))
            q1 = ProductSpec.objects.get(id=product)
            q2 = ValuesSpec.objects.get(id=name_value)
            q3 = Specifications.objects.get(id=name_characteristic)
            q4 = CategoryProducts.objects.get(id='1')
            # print(q)
            q = CharacteristicValue(name_product=q1, name_spec=q3, name_value=q2, cat=q4)
            q.save()

            return JsonResponse({"result": 1})

        elif read_get == '6':
            name_characteristic = (request.GET.get('id_characteristic'))
            product = (request.GET.get('id_product'))
            q = CharacteristicValue.objects.filter(id=name_characteristic, name_product=product)
            q.delete()
            return JsonResponse({"result": 1})
        else:

            id_product = (request.GET.get('product'))
            product = ProductSpec.objects.get(name=id_product)
            pf = ('name_product', 'name_spec', 'name_value')
            features = CharacteristicValue.objects.filter(name_product=product.id).select_related(*pf)

            # spec_id = []
            # for i13 in features:
            #     spec_id.append(i13.name_spec.id)

            # spec_data_list = {}
            # features2 = CharacteristicValue.objects.filter(name_spec__in=spec_id).select_related(*pf)
            #
            # for i241 in features2:
            #     cat_spec = str(i241.name_spec)
            #     value_spec = str(i241.name_value)
            #     if spec_data_list.get(cat_spec) is None:
            #         spec_data_list[cat_spec] = []
            #     else:
            #         spec_data_list[cat_spec].append(value_spec)
            #
            # for key, value in spec_data_list.items():
            #     spec_data_list[key] = list(set(value))

            select_different_values_dict = defaultdict(list)
            for item in features:
                key = str(item.name_spec)
                value = str(item.name_value)
                value_id = str(item.id)
                select_different_values_dict[key].append(value_id)
                select_different_values_dict[key].append(value)

            # return JsonResponse({"result": select_different_values_dict})
            return JsonResponse({"result": select_different_values_dict})


def debug_qur():
    from django.db import connection
    p = '=' * 100
    print(p)
    # print('запросов выполнено: ', len(connection.queries))
    i2 = 0
    for i in connection.queries:
        i2 += 1
        print(f'запрос: №{i2} \r\n\n{i}\r\n\n')
    print(p)


@method_decorator(csrf_exempt, name='dispatch')
class addCharacteristicAjax(View):
    """Создание новых характеристик из запроса"""
    @staticmethod
    def get(request):
        _q = Product.objects.filter(name_spec='', available=True).exclude(url_spec=None)[:5]
        _q = _q.values_list('name', 'category__slug', 'url_spec')
        result = {_i[0]: {'category': _i[1], 'url': _i[2]} for _i in _q}

        # result = {'Xiaomi 12 12/256Gb Pro Lite Blue': {
        #     'category': 'smartfony',
        #     'url': 'https://www.mvideo.ru/products/smartfon-xiaomi-12-12-256gb-pro-lite-blue-400004642/specification'
        # }}

        return JsonResponse(result, safe=True)

    @staticmethod
    def post(request):
        if DEBUG == False and request.headers['X-Tokenauth'] != TOKEN_SPEC:
            return HttpResponse(status=401)

        data = urllib.parse.unquote_plus(request.body.decode('utf-8')[5:])
        data = json.loads(data)

        # Поиск характеристик и значений
        for _product in data:
            spec_list = []
            value_list = []
            for _name, _spec in _product.items():

                for item in _spec:
                    spec_list.append(str(item[0]))
                    value_list.append(str(item[1]))

            obj = RecordingUniqueValues(spec_list=spec_list, value_list=value_list,
                                        product=_product, product_name=_name)
            obj.spec()
            obj.value()
            obj.write()

        return JsonResponse({"result": "ok"})
