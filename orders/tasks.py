from django.core.mail import send_mail
from .models import Order
from myshop.celery import app


@app.task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ № {order_id}'
    message = f'Здравствуйте!\n\nВаш заказ успешно создан. Заказа № {order.id}'

    mail_sent = send_mail(subject, message, 'admin@ch-shop.ru', [order.email])
    return mail_sent
