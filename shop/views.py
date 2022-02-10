from django.core.cache import cache

from specifications.models import CharacteristicValue
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Q


class CategoryDetailView2(ListView):
    model = Product
    context_object_name = 'category_products'
    template_name = 'shop/product_list/cat_product_list.html'
    slug_url_kwarg = 'slug'
    paginate_by = 4

    @staticmethod
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
        context['categories'] = Category.objects.get(slug=self.kwargs.get(self.slug_url_kwarg, None))
        return context

    def get_queryset(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        # Категория товаров
        url_kwargs = {}
        q_condition_queries = Q()
        # Поиск get параметров,фильтрация и запись в масив
        for item in self.request.GET:
            if item != 'price_sort' and item != 'page':
                url_kwargs[item] = self.request.GET.getlist(item)

        if len(url_kwargs) != 0:
            for key, value in url_kwargs.items():
                if isinstance(value, list):  # Является ли переданный обьект листом
                    q_condition_queries.add(Q(**{'value__in': value}), Q.OR)
                else:
                    q_condition_queries.add(Q(**{'value': value}), Q.OR)

            pda = cache.get('pda')
            if not pda:
                pda = Product.objects.all().only('name_spec')
                cache.set('pda', pda, 600)

            p1 = (i.name_spec for i in pda)
            pf = ('name_value', 'name_spec', 'name_product')
            f = CharacteristicValue.objects.filter(name_product__name__in=p1).select_related(*pf)
            data = self.find_get(f, url_kwargs)

            # Запрос для получения товаров
            queryset = Product.objects.filter(name_spec__in=[pf_ for pf_ in data]).select_related(
                'category').prefetch_related('productimage_set')
        else:
            queryset = Product.objects.filter(category__slug=slug).select_related(
                'category').prefetch_related('productimage_set')
        return queryset


class ProductDetailView(DetailView):
    model = Product  # Модель шаблона
    template_name = 'shop/product_detail/product.html'  # Путь и имя шаблона
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

    def get_queryset(self):
        queryset = Product.objects.select_related('category')
        queryset = queryset.prefetch_related('productimage_set').filter(available=True)
        context = []
        image = None
        for i in queryset:
            for i2 in i.productimage_set.all():
                if i2.is_main:
                    image = i2.image
            context.append({'name': i.name, 'price': i.price, 'image': image, 'get_absolute_url': i.get_absolute_url()})
        return context


class BuyingUp(TemplateView):
    template_name = 'shop/buying_up/buying_up.html'


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/product_category/category.html'
    context_object_name = 'categories'
