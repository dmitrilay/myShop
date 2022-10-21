from itertools import product
import json
from multiprocessing.sharedctypes import Value
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from account.models import FavoriteProduct

from specifications.models import CharacteristicValue
from .models import Category, Product, Slider
from cart.forms import CartAddProductForm
from django.views.generic import DetailView, ListView, TemplateView, View
from django.db.models import Q


from django.db.models import Max, Min

from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Count


class FilterAjax(View):
    def get(request, _p):
        _get = _p.GET.get('cat')
        _get = _get[0:-1].split('/')[-1]

        _vl = ('name_spec', 'id',)
        product = Product.objects.filter(category__slug=_get, available=True).exclude(name_spec='').values_list(*_vl)

        # кеш
        resultMinMax_cache = cache.get('resultMinMax_cache')
        if not resultMinMax_cache:
            resultMinMax_cache = Product.objects.aggregate(Min("price"), Max("price"))
            cache.set('resultMinMax_cache', resultMinMax_cache, 500)
        resultMinMax = resultMinMax_cache

        new_set_product = []
        p_min, p_max = resultMinMax['price__min'], resultMinMax['price__max']
        new_set_product.append(('price_min_max', f'{p_min}-{p_max}', 0.1))
        new_set_product.append(('Состояние', 'Новый', 0.2))
        new_set_product.append(('Состояние', 'Бывший в употреблении', 0.3))

        name_cache = "".join(map(lambda _i: str(_i[1]), product))
        product = list(map(lambda _i: _i[0], product))

        # кеш
        _q_cache = cache.get(name_cache)
        if not _q_cache:
            _q_cache = CharacteristicValue.objects.filter(
                name_product__name__in=product,
                name_spec__participation_filtering=True)
            _q_cache = _q_cache.values_list('name_spec__name', 'name_value__name', 'name_spec__priority_spec')
            cache.set(name_cache, _q_cache, 500)
        _q = _q_cache

        # _q = CharacteristicValue.objects.filter(name_product__name__in=product, name_spec__participation_filtering=True)
        # _q = _q.values_list('name_spec__name', 'name_value__name', 'name_spec__priority_spec')

        _q = list(_q)
        _q = _q + new_set_product
        status = {"status": _q}
        return JsonResponse(status, safe=True)


class CategoryDetailView2(ListView):
    model = Product
    context_object_name = 'category_products'
    template_name = 'shop/product_list/product_list.html'
    slug_url_kwarg = 'slug'
    paginate_by = 12

    @ staticmethod
    def find_get(f, url_kwargs):
        """Поиск товара по get запросу"""
        dict_spec_test = {}
        for i in f:
            for key, value in url_kwargs.items():
                if i.name_spec.name == key:
                    if i.name_value.name in value:
                        if not dict_spec_test.get(i.name_product):
                            dict_spec_test[i.name_product] = 0

                        c = dict_spec_test[i.name_product] + 1
                        dict_spec_test[i.name_product] = c
        return dict_spec_test.keys()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # кеш
        cat_cache = cache.get(self.kwargs['slug'])
        if not cat_cache:
            cat_cache = Category.objects.get(slug=self.kwargs.get(self.slug_url_kwarg, None))
            cache.set(self.kwargs['slug'], cat_cache, 500)

        context['categories'] = cat_cache

        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context

    def get_queryset(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        price_min, price_max, condition, _sort = 0, 0, 0, ''
        dict_get = dict(self.request.GET)

        if dict_get.get('page'):
            dict_get.pop('page')

        if dict_get.get('priceMin'):
            price_min = dict_get['priceMin'][0]
            dict_get.pop('priceMin')

        if dict_get.get('priceMax'):
            price_max = dict_get['priceMax'][0]
            dict_get.pop('priceMax')

        if dict_get.get('sort'):
            _sort = dict_get['sort'][0]
            dict_get.pop('sort')

        _condition = []
        if dict_get.get('Состояние'):
            condition = dict_get['Состояние']
            if 'Бывший в употреблении' in condition:
                _condition.append('used')
            if 'Новый' in condition:
                _condition.append('new')

            dict_get.pop('Состояние')

        if dict_get:
            _p_all = Product.objects.exclude(name_spec__in=['', '0']).filter(category__slug=slug, available=True)
            if price_min and price_max:
                _p_all = _p_all.filter(price__gte=price_min, price__lte=price_max)

            if _condition:
                _p_all = _p_all.filter(condition__in=_condition)

            all_product = _p_all.values_list('name_spec')

            result = []
            for _i in dict_get.values():
                result.extend(_i)

            _q1 = Q(name_product__name__in=all_product)
            _q2 = Q(name_value__name__in=result)
            _values_list = ('name_product__name', 'name_spec__name', 'name_value__name')
            _r = CharacteristicValue.objects.filter(_q1, _q2).values_list(*_values_list)

            dict_test = {}
            for spec, value in dict_get.items():
                for item in _r:
                    if spec in item:
                        if dict_test.get(item[0]):
                            dict_test[item[0]] += 1
                        else:
                            dict_test[item[0]] = 1

            _yes = len(dict_get.keys())

            all_product = list(filter(lambda _i: dict_test[_i] == _yes, dict_test))

            if not all_product:
                # По заданным фильтрам ничего не найдено, выходм из функции!
                return all_product

            # Формируем запрос в базу данных
            _q = Product.objects.filter(name_spec__in=all_product, available=True)
            if _sort == 'price_low':
                _q = _q.order_by('price')
            elif _sort == 'price_high':
                _q = _q.order_by('-price')

            queryset = _q.select_related('category').prefetch_related('productimage_set')
        else:
            all_product = []

        if not all_product:
            _q = Product.objects.filter(category__slug=slug, available=True)
            if price_min and price_max:
                _q = _q.filter(price__gte=price_min, price__lte=price_max)
            if _condition:
                _q = _q.filter(condition__in=_condition)
            if _sort == 'price_low':
                _q = _q.order_by('price')
            elif _sort == 'price_high':
                _q = _q.order_by('-price')
            queryset = _q.select_related('category').prefetch_related('productimage_set')

        return queryset


class ProductDetailView(DetailView):
    model = Product  # Модель шаблона
    template_name = 'shop/product_detail/product_detail.html'  # Путь и имя шаблона
    context_object_name = 'product'  # Какое имя необходимо отображать в шаблоне?
    # slug_field = 'slug' # Как называется slug в шаблоне?
    slug_url_kwarg = 'product_slug'  # Какое имя(slug) искать в url?

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form

        se_re = ('name_value', 'name_spec', 'name_product')
        f = CharacteristicValue.objects.filter(name_product__name=context['object'].name_spec).select_related(*se_re)
        context['spec_wi'] = f
        for i in f:
            if str(i.name_spec).find('Бренд') >= 0:
                context['brand_cast'] = i.name_value
                context['url_cast'] = f"/category/{self.kwargs['category_slug']}/?Бренд={i.name_value}"
                break

        # Избранные товары
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        product = Product.objects.filter(slug=slug, available=True)
        favorit = FavoriteProduct.objects.filter(id_product=product[0].pk)
        context['favorit'] = favorit

        return context

    def get_queryset(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        queryset = Product.objects.filter(slug=slug, available=True)
        queryset = queryset.select_related('category').prefetch_related('productimage_set')
        return queryset


class HomeListView(ListView):
    model = Product
    template_name = 'shop/home_page/home_page.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q_slider = Slider.objects.all()
        context['slider_photo'] = q_slider

        # print(q_slider)

        # Избранные товары
        # slug = self.kwargs.get(self.slug_url_kwarg, None)
        # product = Product.objects.filter(slug=slug, available=True)
        # favorit = FavoriteProduct.objects.filter(id_product=product[0].pk)

        return context

    def get_queryset(self):

        queryset = Product.objects.select_related('category')
        queryset = queryset.prefetch_related('productimage_set').filter(available=True)[0:12]
        context = []
        image = None
        for i in queryset:
            for i2 in i.productimage_set.all():
                if i2.is_main:
                    image = i2.image
                    imageOLD = i2.imageOLD

            context.append({'id': i.id,
                            'name': i.name,
                            'price': i.price,
                           'image': image,
                            'imageOLD': imageOLD,
                            'get_absolute_url': i.get_absolute_url()
                            }
                           )
            print(image, i.id)
        return context


class BuyingUp(TemplateView):
    template_name = 'shop/buying_up/buying_up.html'


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/product_category/category.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(cnt=Count('products')).filter(cnt__gt=0, products__available=True)


@ csrf_exempt
def ProductDetailSpecAjax(request):
    product_name = request.GET.get('product')

    product_name = Product.objects.filter(name=product_name).values('name_spec')

    if product_name:
        product_name = product_name[0]['name_spec']

    values = ['name_spec__subcategory__name', 'name_spec__name',
              'name_value__name',  'name_spec__subcategory__priority']
    obj = CharacteristicValue.objects.filter(name_product__name=product_name).values(*values)

    _spec = list(obj)
    for item in _spec:
        if item['name_spec__subcategory__priority'] == None:
            item['name_spec__subcategory__priority'] = 1000

    _spec = sorted(_spec, key=lambda student: student['name_spec__subcategory__priority'])

    return JsonResponse({"spec": _spec})


def SearchProductAjax(request):
    product_name = request.GET.get('search')
    product_list = []
    if product_name:
        product_name_lower = product_name.lower()
        product_name_title = product_name_lower.title()
        q1 = Q(name__icontains=product_name_lower)
        q2 = Q(name__icontains=product_name_title)
        rez = Product.objects.filter(q1 | q2, available=True)[:10]
        for item in rez:
            product_list.append({'name': item.name, 'url': item.get_absolute_url()})

    return JsonResponse({"product_list": product_list})


class SearchListView(ListView):
    model = Product
    template_name = 'shop/search/product_list.html'
    context_object_name = 'category_products'
    paginate_by = 12

    def get_queryset(self):

        product_name = self.request.GET.get('qu')

        _condition = []
        price_min, price_max, condition, _sort = 0, 0, 0, ''
        dict_get = dict(self.request.GET)

        # ====================================

        if dict_get.get('priceMin'):
            price_min = dict_get['priceMin'][0]

        if dict_get.get('priceMax'):
            price_max = dict_get['priceMax'][0]

        if dict_get.get('sort'):
            _sort = dict_get['sort'][0]

        if dict_get.get('Состояние'):
            condition = dict_get['Состояние']
            if 'Бывший в употреблении' in condition:
                _condition.append('used')
            if 'Новый' in condition:
                _condition.append('new')

        # ===============================================
        # Формируем запрос
        # ===============================================
        product_name_lower = product_name.lower()
        product_name_title = product_name_lower.title()
        q1 = Q(name__icontains=product_name_lower)
        q2 = Q(name__icontains=product_name_title)

        q3 = Q(category__name__icontains=product_name_lower)
        q4 = Q(category__name__icontains=product_name_title)
        _q = Product.objects.filter(q1 | q2 | q3 | q4, available=True)

        if price_min and price_max:
            _q = _q.filter(price__gte=price_min, price__lte=price_max)
        if _condition:
            _q = _q.filter(condition__in=_condition)
        if _sort == 'price_low':
            _q = _q.order_by('price')
        elif _sort == 'price_high':
            _q = _q.order_by('-price')
        queryset = _q.select_related('category').prefetch_related('productimage_set')

        return queryset
