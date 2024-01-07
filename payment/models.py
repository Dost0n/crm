from django.db import models
from utils.models import BaseModel

CLIENTS, PAYMENT, INVESMENTS, WITHDRAWALS = "clients", "payment", "investments", "withdrawals"


class Payment(BaseModel):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(
        "clients.Client", models.SET_NULL, blank=True, null=True, related_name='payments')
    date = models.DateField(blank=True, null=True)
    comment = models.CharField(max_length=191, blank=True, null=True)
    amount = models.FloatField()
    type = models.CharField(max_length=50, blank=True, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    is_discount = models.BooleanField(default=False)
    user = models.ForeignKey(
        'users.User', models.SET_NULL, blank=True, null=True)
    transaction = models.ForeignKey(
        "payment.Transaction", models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.client} - {self.amount} {self.currency} - {self.date}"


class Transaction(BaseModel):
    TRANSACTION_TYPE = (
        (CLIENTS, CLIENTS),
        (PAYMENT, PAYMENT),
        (INVESMENTS, INVESMENTS),
        (WITHDRAWALS, WITHDRAWALS),
    )
    title = models.CharField(max_length=191, blank=True, null=True)
    client = models.ForeignKey(
        "clients.Client", models.SET_NULL, blank=True, null=True)
    type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPE, default=INVESMENTS)
    amount = models.FloatField()
    is_credit = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(
        'users.User', models.SET_NULL, blank=True, null=True)
    refunded_by = models.IntegerField(blank=True, null=True)
    refunded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.client} - {self.amount} {self.type} - {self.date}"
