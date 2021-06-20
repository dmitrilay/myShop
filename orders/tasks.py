from django.core.mail import send_mail
from .models import Order
from myshop.celery import app


@app.task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ № {}'.format(order_id)
    p1 = 'Здравствуйте!'
    p2 = 'Ваш заказ успешно создан. Заказа №' + str(order.id)
    message = p1 + '\n\n' + p2

    mail_sent = send_mail(subject, message, 'dmitrilay@gmail.com', [order.email])
    return mail_sent
