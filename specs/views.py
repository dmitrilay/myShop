from collections import defaultdict

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse

from .models import CategoryFeature, FeatureValidator, ProductFeatures
from .forms import NewCategoryFeatureKeyForm, NewCategoryForm
from shop.models import Category, Product
import json


# -------------------------------------------
# Главная страница
# -------------------------------------------
class BaseSpecView(View):
    """Базовая страница"""

    @staticmethod
    def get(request):
        return render(request, 'base.html', {})


# -------------------------------------------
# Создание новой характеристики
# -------------------------------------------
class CreateNewFeature(View):
    """Создание новой характеристики"""

    @staticmethod
    def get(request):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_feature.html', context)

    @staticmethod
    def post(request):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        if form.is_valid():
            new_category_feature_key = form.save(commit=False)
            new_category_feature_key.category = form.cleaned_data['category']
            new_category_feature_key.feature_name = form.cleaned_data['feature_name']
            new_category_feature_key.save()
        return HttpResponseRedirect('/product-specs/')


# -------------------------------------------
# Создание значения для характеристики
# -------------------------------------------
class CreateNewFeatureValidator(View):
    """Создание значения для характеристики"""

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_validator.html', context)


class CreateFeatureView(View):
    """Создание значения для характеристики 2"""

    @staticmethod
    def get(request):
        category_id = request.GET.get('category_id')
        feature_name = request.GET.get('feature_name')
        value = request.GET.get('feature_value').strip(" ")
        category = Category.objects.get(id=int(category_id))
        feature = CategoryFeature.objects.get(category=category, feature_name=feature_name)
        existed_object, created = FeatureValidator.objects.get_or_create(
            category=category,
            feature_key=feature,
            valid_feature_value=value
        )

        if not created:
            return JsonResponse({
                "error": f"Значение '{value}' уже существует."
            })
        messages.add_message(
            request, messages.SUCCESS,
            f'Значение "{value}" для характеристики '
            f'"{feature.feature_name}" в категории {category.name} успешно создано'
        )
        return JsonResponse({'result': 'ok'})


# -------------------------------------------
# Создание характеристик для ТОВАРА
# -------------------------------------------
class NewProductFeatureView(View):
    """Присвоение характеристики определенному товару"""

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_product_feature.html', context)


class AttachNewFeatureToProduct(View):
    """Выгружаем доступные характеристики для заданного товара"""

    @staticmethod
    def get(request):
        product_id = Product.objects.get(id=int(request.GET.get('product_id')))
        existing_features = list(set([item.feature.feature_name for item in product_id.features.all()]))
        print(existing_features)
        category_features = CategoryFeature.objects.filter(
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
        feature_key = CategoryFeature.objects.get(category=category, feature_name=feature_name)
        validators_qs = FeatureValidator.objects.filter(category=category, feature_key=feature_key)

        dict_result = dict()
        for item in validators_qs:
            dict_result[item.id] = [item.id, item.valid_feature_value]

        json_string = json.dumps(dict_result)
        return JsonResponse({"features": json_string})


class CreateNewProductFeatureAjaxView(View):
    """Создаем характеристику для товара"""

    @staticmethod
    def get(request):
        product = Product.objects.get(name=request.GET.get('product'))
        feature_name = request.GET.get('category_feature')
        value = request.GET.get('value')
        category_feature = CategoryFeature.objects.get(category=product.category, feature_name=feature_name)
        feature = ProductFeatures.objects.create(feature=category_feature, product=product, value=value)
        product.features.add(feature)
        return JsonResponse({"OK": "OK"})


# -------------------------------------------
# Унивирсальные классы
# -------------------------------------------
class SearchProductAjaxView(View):
    """Динамический поиск товара по имени"""

    @staticmethod
    def get(request):
        query = request.GET.get('query')
        category_id = request.GET.get('category_id')
        category = Category.objects.get(id=int(category_id))
        products = list(Product.objects.filter(category=category, name__icontains=query).values())
        return JsonResponse({"result": products})


class FeatureChoiceView(View):
    """Выгружает характеристики для определенной категории"""

    @staticmethod
    def get(request):
        category_id = int(request.GET.get('category_id'))
        feature_key_qs = CategoryFeature.objects.filter(category_id=category_id)
        result_dict = dict()
        for item in feature_key_qs:
            result_dict[item.feature_name] = item.feature_name
        return JsonResponse({"result": result_dict, "value": category_id})


# -------------------------------------------
# Остальное
# -------------------------------------------
class UpdateProductFeaturesView(View):
    @staticmethod
    def get(request):
        pass
        # categories = Category.objects.all()
        # context = {'categories': categories}
        # return render(request, 'update_product_features.html', context)


class ShowProductFeaturesForUpdate(View):
    @staticmethod
    def get(request):
        pass
        # product = Product.objects.get(id=int(request.GET.get('product_id')))
        # features_values_qs = product.features.all()
        # print('\n\n\n')
        # print(product)
        #
        # head = """
        # <hr>
        #     <div class="row">
        #         <div class="col-md-4">
        #             <h4 class="text-center">Характеристика</h4>
        #         </div>
        #         <div class="col-md-4">
        #             <h4 class="text-center">Текущее значение</h4>
        #         </div>
        #         <div class="col-md-4">
        #             <h4 class="text-center">Новое значение</h4>
        #         </div>
        #     </div>
        # <div class='row'>{}</div>
        # <div class="row">
        # <hr>
        # <div class="col-md-4">
        # </div>
        # <div class="col-md-4">
        #     <p class='text-center'><button class="btn btn-success" id="save-updated-features">Сохранить</button></p>
        # </div>
        # <div class="col-md-4">
        # </div>
        # </div>
        # """
        # option = '<option value="{value}">{option_name}</option>'
        # select_values = """
        #     <select class="form-select" name="feature-value" id="feature-value" aria-label="Default select example">
        #         <option selected>---</option>
        #         {result}
        #     </select>
        #             """
        # mid_res = ""
        # select_different_values_dict = defaultdict(list)
        # for item in features_values_qs:
        #     fv_qs = FeatureValidator.objects.filter(category=item.product.category, feature_key=item.feature).values()
        #
        #     for fv in fv_qs:
        #         if fv['valid_feature_value'] == item.value:
        #             pass
        #         else:
        #             select_different_values_dict[fv['feature_key_id']].append(fv['valid_feature_value'])
        #     feature_field = '<input type="text" class="form-control" id="{id}" value="{value}" disabled/>'
        #     current_feature_value = """
        #     <div class='col-md-4 feature-current-value' style='margin-top:10px; margin-bottom:10px;'>{}</div>
        #                             """
        #     body_feature_field = """
        #     <div class='col-md-4 feature-name' style='margin-top:10px; margin-bottom:10px;'>{}</div>
        #                         """
        #     body_feature_field_value = """
        #     <div class='col-md-4 feature-new-value' style='margin-top:10px; margin-bottom:10px;'>{}</div>
        #     """
        #     body_feature_field = body_feature_field.format(
        #         feature_field.format(id=item.feature.id, value=item.feature.feature_name))
        #     current_feature_value_mid_res = ""
        #     for item_ in select_different_values_dict[item.feature.id]:
        #         current_feature_value_mid_res += option.format(value=item.feature.id, option_name=item_)
        #     body_feature_field_value = body_feature_field_value.format(
        #         select_values.format(item.feature.id, result=current_feature_value_mid_res)
        #     )
        #     current_feature_value = current_feature_value.format(
        #         feature_field.format(id=item.feature.id, value=item.value))
        #     m = body_feature_field + current_feature_value + body_feature_field_value
        #     mid_res += m
        # result = head.format(mid_res)
        # return JsonResponse({"result": result})


class UpdateProductFeaturesAjaxView(View):
    @staticmethod
    def post(request):
        pass
        # features_names = request.POST.getlist('features_names')
        # features_current_values = request.POST.getlist('features_current_values')
        # new_feature_values = request.POST.getlist('new_feature_values')
        # data_for_update = [{'feature_name': name, 'current_value': curr_val, 'new_value': new_val} for
        #                    name, curr_val, new_val
        #                    in zip(features_names, features_current_values, new_feature_values)]
        # product = Product.objects.get(title=request.POST.get('product'))
        # for item in product.features.all():
        #     for item_for_update in data_for_update:
        #         if item.feature.feature_name == item_for_update['feature_name']:
        #             if item.value != item_for_update['new_value'] and item_for_update['new_value'] != '---':
        #                 cf = CategoryFeature.objects.get(
        #                     category=product.category,
        #                     feature_name=item_for_update['feature_name']
        #                 )
        #                 item.value = FeatureValidator.objects.get(
        #                     category=product.category,
        #                     feature_key=cf,
        #                     valid_feature_value=item_for_update['new_value']
        #                 ).valid_feature_value
        #                 item.save()
        # messages.add_message(
        #     request, messages.SUCCESS,
        #     f'Значения характеристик для товара {product.name} успешно обновлены'
        # )
        # return JsonResponse({"result": "ok"})
