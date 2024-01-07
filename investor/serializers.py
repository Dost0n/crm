from rest_framework import serializers
from investor.models import Investor, Investment
from users.serializers import UserSerializer


class InvestorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    balance = serializers.FloatField(read_only=True)
    consumption = serializers.FloatField(read_only=True)
    coming = serializers.FloatField(read_only=True)
    remainder = serializers.FloatField(read_only=True)
    expected_income = serializers.FloatField(read_only=True)
    real_income = serializers.FloatField(read_only=True)

    class Meta:
        model = Investor
        fields = (
            'id',
            'fullname',
            'phone_number',
            'currency',
            'investor_status',
            'balance',
            'consumption',
            'coming',
            'remainder',
            'expected_income',
            'real_income',
        )


class InvestmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    investor = InvestorSerializer(read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Investment
        fields = (
            'id',
            'investor',
            'transaction',
            'amount',
            'is_credit',
            'date',
            'user',
            'comment',
            'type',
        )


class InvestmentDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    investor_id = serializers.IntegerField(write_only=True)
    amount = serializers.FloatField(required=True)
    type = serializers.IntegerField(required=True)

    def validate_investor_id(self, value):
        if not Investor.objects.filter(id=value).exists():
            raise serializers.ValidationError('Investor not found')
        return value

    class Meta:
        model = Investment
        fields = (
            'id',
            'investor_id',
            'transaction',
            'amount',
            'is_credit',
            'date',
            'user',
            'comment',
            'type',
        )


class InvestorDetailSerializer(serializers.ModelSerializer):
    from clients.serializers import ClientListSerializer
    id = serializers.IntegerField(read_only=True)
    investor_status = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    balance = serializers.FloatField(read_only=True)
    refill = serializers.FloatField(read_only=True)
    withdraw = serializers.FloatField(read_only=True)
    real_income = serializers.FloatField(read_only=True)
    investments = InvestmentDetailSerializer(many=True, read_only=True)
    clients = ClientListSerializer(many=True, read_only=True)
    expected_income = serializers.FloatField(read_only=True)
    consumption = serializers.FloatField(read_only=True)
    coming = serializers.FloatField(read_only=True)
    remainder = serializers.FloatField(read_only=True)

    class Meta:
        model = Investor
        fields = (
            'id',
            'fullname',
            'phone_number',
            'currency',
            'balance',
            'refill',
            'withdraw',
            'investments',
            'investor_status',
            'user',
            'clients',
            'expected_income',
            'real_income',
            'consumption',
            'remainder',
            'coming'
        )
