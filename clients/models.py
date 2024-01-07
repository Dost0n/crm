from django.db import models
from utils.models import BaseModel
from datetime import timedelta, datetime
import random
from users.models import User
from django.core.validators import FileExtensionValidator, MaxLengthValidator


PHONE_EXPIRE_MINUTE = 2
ACTIVE, DEACTIVE = ("active", 'deactive')

class Client(BaseModel):
    CLIENT_STATUS = (
        (ACTIVE, ACTIVE),
        (DEACTIVE, DEACTIVE),
    )
    fullname = models.CharField(max_length=200)
    passport  = models.CharField(max_length=20)
    pinfl    = models.CharField(max_length=14)
    phone_number = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20)
    status = models.CharField(
        max_length=31, choices=CLIENT_STATUS, default=DEACTIVE)
    investor = models.ForeignKey("investor.Investor", on_delete=models.SET_NULL, blank=True, null=True, related_name='clients')
    contract = models.CharField(unique=True, max_length=120, blank=True, null=True)
    product = models.CharField(max_length=191, blank=True, null=True)
    product_code = models.CharField(max_length=20, blank=True, null=True)
    contract_date = models.DateField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    product_price = models.FloatField(blank=True, null=True)
    loan_amount = models.FloatField(blank=True, null=True)
    consumption = models.FloatField(blank=True, null=True)
    initial_payment = models.FloatField(blank=True, null=True)
    percentage = models.FloatField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    total_debit = models.FloatField(blank=True, null=True)
    current_debit = models.FloatField(blank=True, null=True)
    income_amount = models.FloatField(blank=True, null=True)
    real_income = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def create_verify_code(self):
        code = "".join([str(random.randint(0,100) % 10) for _ in range(4)])
        ClientConfirmation.objects.create(
            client_id = self.id,
            code = code)
        return code


class ClientConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(null=True)
    is_isconfirmed = models.BooleanField(default=False)
    client = models.ForeignKey("clients.Client", on_delete=models.CASCADE, related_name='verify_codes')

    def __str__(self):
        return str(self.client.__str__())

    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE_MINUTE)
        super(ClientConfirmation, self).save(*args, **kwargs)


class File(BaseModel):
    file = models.FileField(upload_to='clients/', validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])
    client = models.ForeignKey("clients.Client", on_delete=models.DO_NOTHING)


class Graphic(BaseModel):
    client = models.ForeignKey("clients.Client", on_delete=models.DO_NOTHING,
                                    blank=True, null=True, related_name='graphics')
    amount = models.FloatField(blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    remaining_amount = models.FloatField(blank=True, null=True)
    month = models.DateField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    is_calc =  models.IntegerField(blank=True, null=True)
    delayed =  models.IntegerField(blank=True, null=True)
