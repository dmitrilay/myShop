from django.shortcuts import render, get_object_or_404

from specifications.models import CharacteristicValue, ProductSpec
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from specs.models import ProductFeatures
from django.db.models import Q


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'shop/product_list/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        url_kwargs = {}
        q_condition_queries = Q()
        context['categories'] = self.model.objects.all()

        # ------------------------------
        # Параметры запроса
        # ------------------------------
        get_list = {}
        for item in self.request.GET:
            get_list[item] = self.request.GET.getlist(item)

        if not self.request.GET:
            products = category.products.order_by('price')
        # elif get_list.get('page') or get_list.get('price_sort') and len(get_list) <= 2:
        #     try:
        #         if get_list['price_sort'][0] == '1':
        #             products = category.products.order_by('price')
        #         elif get_list['price_sort'][0] == '2':
        #             products = category.products.order_by('-price')
        #     except Exception:
        #         products = category.products.order_by('price')

        else:
            for item in self.request.GET:
                if len(self.request.GET.getlist(item)) > 1:
                    url_kwargs[item] = self.request.GET.getlist(item)
                else:
                    url_kwargs[item] = self.request.GET.get(item)

            for key, value in url_kwargs.items():
                if key != 'price_sort' and key != 'page':
                    if isinstance(value, list):
                        q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
                    else:
                        q_condition_queries.add(Q(**{'value': value}), Q.OR)

            # print(q_condition_queries)

            if len(q_condition_queries) > 0:
                # cтарый код
                # pf = ProductFeatures.objects.filter(q_condition_queries).prefetch_related('product', 'feature').values(
                #     'product_id')

                # products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
                # print(products)
                # ========================================
                # новый код

                # q_condition_queries2 = Q()
                # test = []
                # for key, value in url_kwargs.items():
                #     if not key == 'price_sort':
                #         # print(key, value)
                #         # q_condition_queries2.add(Q(name_value__name=value), Q.OR)
                #         q_condition_queries2.add(Q(name_value__name=value), Q.OR)
                #         test.append(Q(name_value__name=value))

                pda = Product.objects.all()

                p1 = (i.name_spec for i in pda)
                f = CharacteristicValue.objects.filter(name_product__name__in=p1).prefetch_related(
                    'name_value', 'name_spec', 'name_product')

                dict_spec_test = {}
                for i in f:
                    for key, value in url_kwargs.items():
                        if not key == 'price_sort':
                            if i.name_spec.name == key:
                                if i.name_value.name in value:
                                    if not dict_spec_test.get(i.name_product):
                                        dict_spec_test[i.name_product] = 0

                                    c = dict_spec_test[i.name_product] + 1
                                    dict_spec_test[i.name_product] = c

                # =========================================
                # Узнаем кол-во параметров в фильтре
                len_pr = len(url_kwargs.values())
                if url_kwargs.get('price_sort'):
                    if url_kwargs.get('page'):
                        max_v = len_pr - 2
                    else:
                        max_v = len_pr - 1
                else:
                    max_v = len_pr
                # Конец
                # =========================================

                orm_z = []
                for key, value in dict_spec_test.items():
                    if value == max_v:
                        orm_z.append(key)

                products = Product.objects.filter(name_spec__in=[pf_ for pf_ in orm_z])
                # products = orm_z
                # Конец нового кода
                # ========================================
                # products = category.products.all()
            else:
                products = category.products.all()

            if get_list.get('price_sort'):
                if get_list['price_sort'][0] == '2':
                    products = products.order_by('-price')
                else:
                    products = products.order_by('price')
            else:
                products = products.order_by('price')

        # =========================================
        # paginator
        paginator = Paginator(products, 3)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = page.previous_page_number()
        else:
            prev_url = ''
        if page.has_next():
            next_url = page.next_page_number()
        else:
            next_url = ''

        context['next_url'] = next_url
        context['prev_url'] = prev_url
        context['is_paginated'] = is_paginated
        context['products'] = page

        # ==============================
        # Return
        # ==============================
        # context['category_products'] = products
        context['category_products'] = page
        return context


class ProductDetailView(DetailView):
    model = Product  # Модель шаблона
    template_name = 'product_2/product.html'  # Путь и имя шаблона
    context_object_name = 'product'  # Какое имя необходимо отображать в шаблоне?
    # slug_field = 'slug' # Как называется slug в шаблоне?
    slug_url_kwarg = 'product_slug'  # Какое имя(slug) искать в url?

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context

    def get_queryset(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        queryset = Product.objects.filter(slug=slug, available=True)
        return queryset


class HomeListView(ListView):
    model = Product
    template_name = 'shop/home_page/home_page.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True).select_related('category')


class BuyingUp(TemplateView):
    template_name = 'shop/buying_up/buying_up.html'


class CategoryListView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'

# ---------------------
# --- Архив ---
# ---------------------
# def product_detail(request, category_slug, product_slug):
#     product = get_object_or_404(Product, slug=product_slug, available=True)
#     cart_product_form = CartAddProductForm()
#     context = {'product': product, 'cart_product_form': cart_product_form}
#     return render(request, 'product_2/product.html', context)

# class CategoryListView(ListView):
#     model = Category
#     template_name = 'category.html'
#     context_object_name = 'categories'
#
#     queryset = Category.objects.all()
#     context_object_name = 'category'
#     slug_url_kwarg = 'slug'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = queryset = Category.objects.all()
#         return context
#
#     def get_queryset(self):
#         pass


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#
#     # ------------------------------paginator
#     paginator = Paginator(products, 4)
#
#     page_number = request.GET.get('page', 1)
#     page = paginator.get_page(page_number)
#
#     is_paginated = page.has_other_pages()
#
#     if page.has_previous():
#         prev_url = '?page={}'.format(page.previous_page_number())
#     else:
#         prev_url = ''
#
#     if page.has_next():
#         next_url = '?page={}'.format(page.next_page_number())
#     else:
#         next_url = ''
#     # ------------------------------
#     context = {'category': category,
#                'categories': categories,
#                'products': page,
#                'is_paginated': is_paginated,
#                'next_url': next_url,
#                'prev_url': prev_url}
#
#     return render(request, 'product/list.html', context)
