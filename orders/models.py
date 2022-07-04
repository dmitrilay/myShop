from django.db import models
from shop.models import Product
from account.models import Profile


class Order(models.Model):
    first_name = models.CharField(max_length=50, default='Guest', blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    # profile = models.ForeignKey(Profile, related_name='user_item', on_delete=models.CASCADE, blank=True)
    profile = models.CharField(max_length=50, blank=True)
    sum_order = models.IntegerField(default=0, verbose_name='Сумма заказа')

    def save(self, *args, **kwargs):
        sum = 0
        for item in self.items.all():
            sum += item.get_cost()

        if sum != 0:
            self.sum_order = sum
        super(Order, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
