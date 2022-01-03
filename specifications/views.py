import json
import os
from collections import defaultdict
from pyexpat.errors import messages

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView

from myshop.settings import BASE_DIR
from shop.models import Category, Product
from .forms import NewCategoryFeatureKeyForm
from .models import *


class AllSpecView(View):
    @staticmethod
    def get(request):
        categories = CategoryProducts.objects.all()
        print(categories)
        context = {'categories': categories}
        return render(request, 'specs/new_product_feature.html', context)


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
class CreateNewFeature(FormView):
    template_name = 'specs/new_feature.html'
    form_class = NewCategoryFeatureKeyForm
    context_object_name = 'form'
    success_url = '/spec/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# -------------------------------------------
# Создание значения для характеристики
# -------------------------------------------
class CreateNewFeatureValidator(View):

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'specs/new_validator.html', context)


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
        feature_name = request.GET.get('product_feature_name')
        feature_key = CategoryProducts.objects.get(category=category, feature_name=feature_name)
        validators_qs = FeatureValidator.objects.filter(category=category, feature_key=feature_key)

        dict_result = dict()
        for item in validators_qs:
            dict_result[item.id] = [item.id, item.valid_feature_value]

        json_string = json.dumps(dict_result)
        return JsonResponse({"features": json_string})


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
        # print('---------------')
        # print('---------------')
        # print('---------------')
        # print('---------------')
        # print('---------------')
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
        id_product = (request.GET.get('product'))
        product = ProductSpec.objects.get(name=id_product)
        pf = ('name_product', 'name_spec', 'name_value')
        features = CharacteristicValue.objects.filter(name_product=product.id).select_related(*pf)

        select_different_values_dict = defaultdict(list)
        for item in features:
            select_different_values_dict[str(item.name_spec)] = str(item.name_value)

        return JsonResponse({"result": select_different_values_dict})
