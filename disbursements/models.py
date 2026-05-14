from django.db import models
from django.conf import settings
from applications.models import Application

class Disbursement(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'

    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='disbursement')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='Bank Transfer')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Disbursement for {self.application}"
