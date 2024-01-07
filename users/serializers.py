from users.models import User, ACTIVE, DEACTIVE
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from utils.confirmation import validate_phone
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    phone_number = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','phone_number', 'auth_status', 'user_role')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'user_role', 'auth_status')


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.auth_status = ACTIVE
        user.set_password(validated_data['password'])
        user.save()
        return user

        
    def validate_phone_number(self, value):
        value = validate_phone(value)
        if value and User.objects.filter(phone_number=value).exists():
            raise ValidationError("Bunday foydalanuvchi mavjud!")
        return value

    def to_representation(self, instance):
        data = super(CreateUserSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class ChangeUserInformationSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if password:
            validate_password(password)

        if password != confirm_password:
            raise ValidationError(
                {
                    'message': "Parolingiz va tasdiqlash parolingiz bir biriga teng emas"
                }
            )
        return data

    def validate_first_name(self, first_name):
        if len(first_name) < 1 or len(first_name) > 30:
            raise ValidationError(
                {
                    'message': "Ism 1 dan 30 gacha harflar ketma-ketligidan iborat bo'lishi kerak."
                }
            )
        if first_name.isdigit():
            raise ValidationError(
                {
                    'message': "Ism raqamlardan iborat bo'lmasligi kerak!"
                }
            )
        return first_name

    def validate_last_name(self, last_name):
        if len(last_name) < 1 or len(last_name) > 30:
            raise ValidationError(
                {
                    'message': "Familiya 1 dan 30 gacha harflar ketma-ketligidan iborat bo'lishi kerak."
                }
            )
        if last_name.isdigit():
            raise ValidationError(
                {
                    'message': "Familiya raqamlardan iborat bo'lmasligi kerak!"
                }
            )
        return last_name

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def auth_validate(self, data):
        phone_number = data.get("phone_number")
        phone_number = validate_phone(phone_number)
        user = authenticate(
            self.context['request'], phone_number=phone_number, password=data.get('password'))
        if user is None:
            raise ValidationError(
                {
                    'success': False,
                    "message": "Telefon raqam yoki parol xato!"
                }
            )
        if user is not None and user.auth_status == DEACTIVE:
            raise ValidationError(
                {
                    'success': False,
                    "message": " Foydalanuvchi active holatda emas!"
                }
            )

        self.user = user

    def validate(self, data):
        self.auth_validate(data)
        data = self.user.token()
        data['full_name'] = self.user.full_name
        return data

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError(
                {
                    "message": "Foydalanuvchi mavjud emas!"
                }
            )
        return users.first()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ChangeUserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if password:
            validate_password(password)

        if password != confirm_password:
            raise ValidationError(
                {
                    'message': "Parolingiz va tasdiqlash parolingiz bir biriga teng emas"
                }
            )
        return data
