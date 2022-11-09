# from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import JsonResponse, FileResponse
from shop.models import Slider, ProductImage
import uuid


@method_decorator(csrf_exempt, name='dispatch')
class photo_replacement_api_viev(View):
    @staticmethod
    def post(request):
        if request.FILES:
            name_obj = request.FILES['file_jpg'].name.split('.')[0]
            id, name_obj = name_obj.split('_')
            obj = ProductImage.objects.get(id=id)
            obj.image.delete()
            obj.imageOLD.delete()
            obj.image = request.FILES['file_webp']
            obj.imageOLD = request.FILES['file_jpg']
            obj.compression = True
            obj.save()

        status = {"status": 200}
        return JsonResponse(status, safe=False)

    @staticmethod
    def get(request):
        obj = ProductImage.objects.filter(compression=False)[:1]

        file_name, file_image, id = obj[0].name, obj[0].image, obj[0].id

        return FileResponse(open(file_image.path, 'rb'), filename=f"{id}_{file_name}")
