from collections import defaultdict
from django import template
from django.utils.safestring import mark_safe
from specifications.models import *
from shop.models import *
from django.db.models import Q
from django.core.cache import cache

register = template.Library()


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
        pf = CharacteristicValue.objects.filter(q_condition_queries, name_spec__participation_filtering=True)
        product_features = pf.select_related('name_value', 'name_spec').order_by('name_spec__priority_spec')
        cache.set('product_features', product_features, 600)

    get_list = context['request'].GET

    for pf in product_features:
        pr_1, pr_2 = pf.name_spec.name, pf.name_value.name
        if pr_2 not in feature_and_values[pr_1, pr_1]:
            feature_and_values[pr_1, pr_1].append(pr_2)

    search_filter_body = """<div class="col-md-12">{}</div>"""
    gl = 0
    if get_list.get('price_sort'):
        gl = get_list['price_sort']
    p1 = f'<option value="1" {"selected" if gl == "1" else ""}>Сначало дешевле</option>'
    p2 = f'<option value="2" {"selected" if gl == "2" else ""}>Сначало дороже</option>'
    mid_res = f'<select class="form-select" name="price_sort">{p1}{p2}</select>'

    mid_res += '<hr>'

    for (feature_name, feature_filter_name), feature_values in feature_and_values.items():
        feature_name_html = f"""<p>{feature_name}</p>"""
        feature_values_res = ""
        for f_v in feature_values:
            ch = ''
            if get_list.get(feature_name):
                if f_v in get_list.getlist(feature_name):
                    ch = 'checked'

            mid_feature_values_res = \
                f"<input type='checkbox' name='{feature_filter_name}' value='{f_v}' {ch}> {f_v}"
            mid_feature_values_res = \
                f'<p>{mid_feature_values_res}</p>'
            feature_values_res += mid_feature_values_res
        feature_name_html += feature_values_res
        mid_res += feature_name_html + '<hr>'

    res = search_filter_body.format(mid_res)
    return mark_safe(res)


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


@register.simple_tag(takes_context=True)
def spec(context, page=1):
    f = CharacteristicValue.objects.filter(name_product__name=context['object'].name_spec).prefetch_related(
        'name_value', 'name_spec', 'name_product')
    p = ''
    for i in f:
        p += f'<div class="text-muted">{i}</div>'
    return mark_safe(p)
