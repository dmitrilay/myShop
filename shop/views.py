from django.shortcuts import render, get_object_or_404
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
        query = self.request.GET.get('search')
        category = self.get_object()
        # context['cart'] = self.cart
        url_kwargs = {}
        q_condition_queries = Q()
        context['categories'] = self.model.objects.all()

        # ------------------------------paginator
        pf = category.products.all()
        paginator = Paginator(pf, 4)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        # print('\n\n')
        # print(is_paginated)
        # print('\n\n')

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        context['next_url'] = next_url
        context['prev_url'] = prev_url
        context['is_paginated'] = is_paginated
        context['category_products'] = page
        context['products'] = page
        return context

        # ------------------------------

        # делаем запрос из сходя из slug
        if not query and not self.request.GET:
            context['category_products'] = category.products.all()
            return context

        # if query:
        #     products = category.product_set.filter(Q(title__icontains=query))
        #     context['category_products'] = products
        #     return context

        # Параметры запроса
        for item in self.request.GET:
            if len(self.request.GET.getlist(item)) > 1:
                url_kwargs[item] = self.request.GET.getlist(item)
            else:
                url_kwargs[item] = self.request.GET.get(item)

        for key, value in url_kwargs.items():
            if isinstance(value, list):
                q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
            else:
                q_condition_queries.add(Q(**{'value': value}), Q.OR)

        pf = ProductFeatures.objects.filter(q_condition_queries).prefetch_related('product', 'feature').values(
            'product_id')

        products = Product.objects.filter(id__in=[pf_['product_id'] for pf_ in pf])
        context['category_products'] = products
        return context


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # ------------------------------paginator
    paginator = Paginator(products, 4)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    # ------------------------------
    context = {'category': category,
               'categories': categories,
               'products': page,
               'is_paginated': is_paginated,
               'next_url': next_url,
               'prev_url': prev_url}

    return render(request, 'product/list.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'product_2/product.html', context)


class HomeListView(ListView):
    model = Product
    template_name = 'shop/home_page/home_page.html'
    context_object_name = 'products'


class BuyingUp(TemplateView):
    template_name = 'shop/buying_up/buying_up.html'


class CategoryListView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'

    # queryset = Category.objects.all()
    # context_object_name = 'category'
    # slug_url_kwarg = 'slug'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = queryset = Category.objects.all()
    #     return context
    #
    # def get_queryset(self):
    #     pass


class ProductDetailView(DetailView):
    model = Product  # Модель шаблона
    template_name = 'test.html'  # Путь и имя шаблона
    context_object_name = 'product'  # Какое имя необходимо отображать в шаблоне?
    # slug_field = 'slug' # Как называется slug в шаблоне?
    slug_url_kwarg = 'product_slug'  # Какое имя(slug) искать в url?

    # queryset = Product.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print('\n\n\n')
    #     print(context)
    #     return context

    # def get_queryset(self, **kwargs):
    #     # print(**kwargs)
    #     # context = super().get_context_data(**kwargs)
    #     # queryset = get_object_or_404(Product, slug=self.slug_url_kwarg, available=True)
    #     # queryset = Product.objects.filter(slug=self.slug_url_kwarg)
    #     # print(context)
    #     return 1
