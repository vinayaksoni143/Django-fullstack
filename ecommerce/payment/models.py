from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class ShippingAddress(models.Model):

    # foreign key
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)

    full_name = models.CharField(max_length = 300)
    email = models.CharField(max_length = 255)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=100)

    # Optional
    state = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return 'Shipping Address - '+str(self.id)

