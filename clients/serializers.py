from rest_framework import serializers
from clients.models import Client, File, Graphic
from payment.models import Payment
from users.serializers import UserSerializer
from utils.confirmation import validate_phone
from rest_framework.exceptions import ValidationError
from investor.models import Investor, Investment, ACTIVE, DEACTIVE
import os
import datetime
from dateutil import relativedelta
from django.shortcuts import get_object_or_404



class ClientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'fullname', "passport", "pinfl",
                  "phone_number", 'phone_number2')

        extra_kwargs = {
            "phone_number2": {"required": False}
        }

    def create(self, validated_data):
        client = super().create(validated_data)
        code = client.create_verify_code()
        client.save()
        return client

    def validate_phone_number(self, value):
        value = validate_phone(value)
        if value and Client.objects.filter(phone_number=value).exists():
            raise ValidationError("Phone number already exists")
        return value

    # def validate_phone_number2(self, value):
    #     value = validate_phone(value)
    #     if value and Client.objects.filter(phone_number=value).exists():
    #         raise ValidationError("Phone number already exists")
    #     return value


class ClientUpdateCreateSerializer(serializers.ModelSerializer):
    investor_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Client
        fields = ("contract", 'investor_id', "product", "product_code", 'contract_date', "payment_date",
                    "product_price", 'initial_payment', "consumption", 'percentage', 'month', "loan_amount",
                    "currency", 'total_debit', 'income_amount', 'current_debit', 'real_income')

    def update(self, instance, validated_data):
        instance.contract = validated_data.get('contract', instance.contract)
        instance.product_code = validated_data.get('product_code', instance.product_code)
        instance.product = validated_data.get('product', instance.product)
        instance.contract_date = validated_data.get('contract_date', instance.contract_date)
        instance.investor_id = validated_data.get('investor_id', instance.investor_id)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)
        instance.product_price = validated_data.get('product_price', instance.product_price)
        instance.initial_payment = validated_data.get('initial_payment', instance.initial_payment)
        instance.consumption = validated_data.get('consumption', instance.consumption)
        instance.percentage = validated_data.get('percentage', instance.percentage)
        instance.month = validated_data.get('month', instance.month)
        instance.loan_amount = validated_data.get('loan_amount', instance.loan_amount)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.total_debit = validated_data.get('total_debit', instance.total_debit)
        instance.income_amount = validated_data.get('income_amount', instance.income_amount)
        instance.current_debit = validated_data.get('current_debit', instance.current_debit)
        instance.real_income = validated_data.get('real_income', instance.real_income)

        if instance.status == DEACTIVE:
            instance.status = ACTIVE
        instance.save()
        client = get_object_or_404(Client, id=instance.id)
        for i in range(1, instance.month+1):
            nextmonth = datetime.date.today() + relativedelta.relativedelta(months=i)
            if i==1:
                is_calc=1
            else:
                is_calc=0
            graphic = Graphic(client = client, amount = instance.current_debit,
                                paid_amount = 0, remaining_amount = instance.current_debit,
                                month = nextmonth, date = nextmonth, is_calc = is_calc, delayed = 0)
            graphic.save()
        investor = Investor.objects.get(id=instance.investor_id)
        investment = Investment(investor=investor, amount=instance.loan_amount, is_credit=False, user=instance.user, type=3)
        investment.save()
        return super(ClientUpdateCreateSerializer, self).update(instance, validated_data)



class ClientListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = (
            'id',
            'fullname',
            'contract',
            'product',
            'total_debit',
            'current_debit',
            'income_amount',
            'real_income',
            'currency',
        )


class ClientSerializer(serializers.ModelSerializer):
    from investor.serializers import InvestorSerializer
    id = serializers.IntegerField(read_only = True)
    user = UserSerializer(read_only=True)
    investor = InvestorSerializer(read_only=True)
    investor_summa = serializers.SerializerMethodField('get_investor_summa')
    remainder_summa = serializers.SerializerMethodField('get_remainder_summa')

    class Meta:
        model = Client
        fields = "__all__"

    
    @staticmethod
    def get_investor_summa(obj):
        if obj.product_price and obj.initial_payment:
            summa = obj.product_price - obj.initial_payment
            return summa
        else:
            return None
    
    @staticmethod
    def get_remainder_summa(obj):
        payments = Payment.objects.all()
        summa = 0
        if len(payments)>0:
            for payment in payments:
                summa+=payment.amount
            return obj.loan_amount-summa
        else:
            return obj.loan_amount



class ClientVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    code = serializers.CharField(write_only=True, required=True)


class ClientNewVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True)


class FileSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField('get_file_path')
    size = serializers.SerializerMethodField('get_file_size')
    client = ClientSerializer()

    class Meta:
        model = File
        fields = ('path', 'size', 'client', 'created_time')

    @staticmethod
    def get_file_path(obj):
        return obj.file.path

    @staticmethod
    def get_file_size(obj):
        return os.path.getsize(obj.file.path)


class GraphicSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    # client = ClientSerializer(read_only=True)
    class Meta:
        model = Graphic
        fields = "__all__"
