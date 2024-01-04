from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    order_id = models.CharField(max_length=255, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255, blank=False, null=True)
    tnx_id = models.CharField(max_length=255, blank=False, null=True)
    val_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=255, blank=False, null=True)
    invoice = models.FileField(upload_to='invoices', blank=True, null=True)
    total_amount = models.FloatField(default=0.0,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.order_id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255, blank=False, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.order.order_id}"