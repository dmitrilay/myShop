from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)
    # favorite = models.ForeignKey('FavoriteProduct', on_delete=models.CASCADE)

    def __str__(self):
        # return '{}'.format(self.user.profile.id)
        return 'Profile {}'.format(self.id)


class FavoriteProduct(models.Model):
    id_product = models.SmallIntegerField(verbose_name='id продукта', blank=True, null=True)
    title_product = models.CharField(max_length=200, verbose_name='Имя продукта', blank=True, null=True)
    profile_favorite = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
