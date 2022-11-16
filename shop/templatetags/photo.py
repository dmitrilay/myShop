from django import template

register = template.Library()


@register.inclusion_tag('common/photo.html', name='picture_tag')
def test_tag_1(image_webp=None, image_jpeg=None):
    plug_webp, plug_jpg = '/static/img/img_default/no_image.webp', '/static/img/img_default/no_image.jpg'
    image_webp = image_webp if image_webp else plug_webp
    plug_jpg = plug_jpg if plug_jpg else plug_jpg
    return {"image_webp": image_webp, "image_jpeg": image_jpeg}
