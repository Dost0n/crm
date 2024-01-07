from django.db import models
from utils.models import BaseModel
from payment.models import Transaction, INVESMENTS, CLIENTS, PAYMENT, WITHDRAWALS

ACTIVE, DEACTIVE = ("active", 'deactive')


class Investor(BaseModel):
    INVESTOR_STATUS = (
        (ACTIVE, ACTIVE),
        (DEACTIVE, DEACTIVE),
    )
    fullname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    chat_id = models.CharField(
        max_length=100, blank=True, null=True)  # telegram
    investor_status = models.CharField(
        max_length=31, choices=INVESTOR_STATUS, default=ACTIVE)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='investors')

    def get_balance(self):
        balance = 0
        for investment in self.investments.all():
            if investment.is_credit:
                balance += investment.amount
            else:
                balance -= investment.amount
        return balance

    def __str__(self):
        return self.fullname



class Investment(BaseModel):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='investments')
    transaction = models.ForeignKey("payment.Transaction", models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    is_credit = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True, auto_now_add=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=191, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)  # 1-popolnenie, 2-snyatie, 3-debit, 4-credit

    def __str__(self):
        return f"{self.investor} - {self.amount} {self.type} - {self.date}"
    
    def save(self, *args, **kwargs):
        if self.type in [1, 4]:
            self.is_credit = True

        if self.type == 1:
            title = "Инвестиции"
            type = INVESMENTS
        elif self.type == 2:
            title = "Снятие средств"
            type = WITHDRAWALS
        elif self.type == 3:
            title = "Контрак"
            type = CLIENTS
        elif self.type == 4:
            title = "Оплата долга"
            type = PAYMENT

        transaction = Transaction.objects.create(
            title=title,
            type=type,
            amount=self.amount,
            date=self.date,
            user=self.user,
            is_credit=self.is_credit
        )
        self.transaction = transaction
        super().save(*args, **kwargs)