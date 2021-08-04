from collections import defaultdict
from django import template
from django.utils.safestring import mark_safe
from specs.models import ProductFeatures

register = template.Library()


@register.filter
def test123(data):
    return f'{data} вот это фильтр'


# @register.filter
@register.simple_tag(takes_context=True)
def product_spec(context, category):
    product_features = ProductFeatures.objects.filter(product__category=category).select_related('feature')
    feature_and_values = defaultdict(list)

    get_list = {}
    # print('================')
    # print(context['request'].GET)
    get_list = context['request'].GET
    # for item in request.GET:
    # get_list[item] = request.GET.getlist(item)

    for pf in product_features:
        p_1 = feature_and_values[(pf.feature.feature_name, pf.feature.feature_filter_name)]
        if pf.value not in p_1:
            feature_and_values[(pf.feature.feature_name, pf.feature.feature_filter_name)].append(pf.value)

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
