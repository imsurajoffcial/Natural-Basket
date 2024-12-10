from django.db import models

# Create your models here.
class Payment(models.Model):
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    amount = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


