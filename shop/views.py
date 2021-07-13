from django.shortcuts import render, get_object_or_404
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.views.generic import DetailView
from specs.models import ProductFeatures
from django.db.models import Q


def category_p1(request):
    category = '131414 ' * 565
    context = {'category': category}

    return render(request, 'shop/category_detail.html', context)


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


def StartPageViews(request):
    products = Product.objects.filter(available=True)[0:8]
    category = 1
    context = {'category': category, 'products': products, }

    return render(request, 'shop/home_page/home_page.html', context)


def skupka(request):
    category = 1
    context = {'category': category}

    return render(request, 'skupka.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category.html', context)
