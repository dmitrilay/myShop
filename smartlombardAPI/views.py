from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def smartlombardAJAX(request):
    _p = request.body.decode()
    # .get('body')
    print(_p)
    # print('test')
    return JsonResponse({"product_list": 'product_list'})


# def SearchProductAjax(request):
#     product_name = request.GET.get('search')

#     product_list = []
#     if product_name:
#         rez = Product.objects.filter(name__icontains=product_name)[:10]
#         for item in rez:
#             product_list.append({'name': item.name, 'url': item.get_absolute_url()})

#     return JsonResponse({"product_list": product_list})
