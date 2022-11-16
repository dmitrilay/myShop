def sterilization_of_products(queryset):
    context = []
    for item in queryset:
        image, imageOLD = None, None
        for i2 in item.productimage_set.all():
            if i2.is_main:
                image, imageOLD = i2.image, i2.imageOLD
                break

        context.append({'id': item.id,
                        'name': item.name,
                        'price': item.price,
                        'image': image,
                        'imageOLD': imageOLD,
                        'get_absolute_url': item.get_absolute_url()
                        })

    return context
