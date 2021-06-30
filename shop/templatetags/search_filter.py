from collections import defaultdict

from django import template
from django.utils.safestring import mark_safe

from specs.models import ProductFeatures

register = template.Library()


@register.filter
def test123(data):
    return f'{data} вот это фильтр'


@register.filter
def product_spec(category):
    product_features = ProductFeatures.objects.filter(product__category=category)
    feature_and_values = defaultdict(list)

    for pf in product_features:
        p_1 = feature_and_values[(pf.feature.feature_name, pf.feature.feature_filter_name)]
        if pf.value not in p_1:
            feature_and_values[(pf.feature.feature_name, pf.feature.feature_filter_name)].append(pf.value)
            # print('\n')
            # print(feature_and_values)

    search_filter_body = """<div class="col-md-12">{}</div>"""
    mid_res = ""

    for (feature_name, feature_filter_name), feature_values in feature_and_values.items():
        feature_name_html = f"""<p>{feature_name}</p>"""
        feature_values_res = ""
        for f_v in feature_values:
            mid_feature_values_res = \
                "<input type='checkbox' name='{f_f_name}' value='{feature_name}'> {feature_name}</br>".format(
                    feature_name=f_v, f_f_name=feature_filter_name
                )
            feature_values_res += mid_feature_values_res
        feature_name_html += feature_values_res
        mid_res += feature_name_html + '<hr>'
    res = search_filter_body.format(mid_res)
    return mark_safe(res)
