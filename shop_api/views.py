# from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import JsonResponse, FileResponse
from shop.models import Slider


@method_decorator(csrf_exempt, name='dispatch')
class photo_replacement_api_viev(View):
    @staticmethod
    def post(request):
        print('-----------')
        print(dir(request))
        s = request.FILES['file']
        Slider.objects.create(name='test', image=s)
        status = {"status": 200}
        return JsonResponse(status, safe=False)

    @staticmethod
    def get(request):
        print('-----------')
        # print(dir(request))
        obj = Slider.objects.get(id='6')
        print(obj.image)
        status = {"status": 200}
        response = FileResponse(open(obj.image.path, 'rb'), )
        # filename=obj.name
        # return JsonResponse(status, safe=False)
        return response
