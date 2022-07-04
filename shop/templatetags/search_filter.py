from collections import defaultdict
from django import template
from django.utils.safestring import mark_safe
from specifications.models import *
from shop.models import *
from django.db.models import Q
from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('shop/product_list/include/filters.html', takes_context=True)
def show_filters(context):
    # feature_and_values = defaultdict(list)

    pda = cache.get('pda')
    if not pda:
        pda = Product.objects.all()
        cache.set('pda', pda, 600)

    q_condition_queries = Q()
    for i in pda:
        q_condition_queries.add(Q(name_product__name=i.name_spec), Q.OR)

    product_features = cache.get('product_features')
    if not product_features:
        pf = CharacteristicValue.objects.filter(q_condition_queries, name_spec__participation_filtering=True)
        product_features = pf.select_related('name_value', 'name_spec').order_by('name_spec__priority_spec')
        cache.set('product_features', product_features, 600)

    get_list = context['request'].GET

    feature_and_values = {}
    for item in product_features:
        spec, value = item.name_spec.name, item.name_value.name
        if not feature_and_values.get(spec):
            feature_and_values[spec] = [value]
        else:
            if not value in feature_and_values[spec]:
                feature_and_values[spec].append(value)

    # Дабовляем get параметры и id для label
    new_dict = {}
    i = 1
    for key, value in feature_and_values.items():
        for item in value:
            if not new_dict.get(key):
                new_dict[key] = [[item, i]]
            else:
                new_dict[key].append([item, i])
            i += 1

    get_list_dict = dict(get_list)
    for key, value in get_list_dict.items():
        if key in new_dict:
            for i in range(len(value)):
                l = len(new_dict[key])
                for i2 in range(l):

                    if new_dict[key][i2][0] == value[i]:
                        new_dict[key][i2].append('checked')

    return {'product_features': new_dict}


@register.simple_tag(takes_context=True)
def product_spec(context, category):
    feature_and_values = defaultdict(list)

    pda = cache.get('pda')
    if not pda:
        pda = Product.objects.all()
        cache.set('pda', pda, 600)

    q_condition_queries = Q()
    for i in pda:
        q_condition_queries.add(Q(name_product__name=i.name_spec), Q.OR)

    product_features = cache.get('product_features')
    if not product_features:
        pf = CharacteristicValue.objects.filter(
            q_condition_queries, name_spec__participation_filtering=True)
        product_features = pf.select_related(
            'name_value', 'name_spec').order_by('name_spec__priority_spec')
        cache.set('product_features', product_features, 600)

    get_list = context['request'].GET

    for pf in product_features:
        pr_1, pr_2 = pf.name_spec.name, pf.name_value.name
        if pr_2 not in feature_and_values[pr_1, pr_1]:
            feature_and_values[pr_1, pr_1].append(pr_2)


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag(takes_context=True)
def page_replace(context, page=1):
    num = ''
    for c in str(page):
        if c.isdigit():
            page = num + c

    context_data = context['request'].GET.copy()
    context_data['page'] = page
    return context_data.urlencode()


# @register.simple_tag(name='images_tag', takes_context=True)
# def images_tag(context, name_product):
#     # se_re = ('name_value', 'name_spec', 'name_product')
#     # f = CharacteristicValue.objects.filter(name_product__name=context['object'].name_spec).select_related(*se_re)
#     return mark_safe('<p>1</p>')

@register.simple_tag()
def images_tag(filter=None):
    obj = ProductImage.objects.filter(product=filter, is_main=True)
    # print(obj)
    return obj[0].image.url
