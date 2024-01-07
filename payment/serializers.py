from rest_framework import serializers
from payment.models import Payment, Transaction
from users.serializers import UserSerializer
from clients.serializers import ClientSerializer


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"


class PaymentCreateSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = (
            'client_id',
            'date',
            'comment',
            'currency',
            'amount',
            'type',
            'is_discount',
        )


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    transaction = TransactionSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id',
            'client',
            'date',
            'comment',
            'currency',
            'amount',
            'type',
            'is_discount',
            'user',
            'transaction',
        )
