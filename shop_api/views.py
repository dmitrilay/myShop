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
        return JsonResponse(status, safe=True)

    @staticmethod
    def get(request):
        if request.GET.get("getcount"):
            obj = ProductImage.objects.filter(compression=False).values('id')
            obj = {"list_image_id": list(obj)}
            res = JsonResponse(obj, safe=False)
        if request.GET.get("get_photo_id"):
            id_photo = request.GET.get("get_photo_id")
            obj = ProductImage.objects.get(id=id_photo)
            file_name, file_image, id = obj.name, obj.image, obj.id
            res = FileResponse(open(file_image.path, 'rb'), filename=f"{id}_{file_name}")

        return res
