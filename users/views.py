from rest_framework.generics import CreateAPIView, UpdateAPIView
from users.serializers import (CreateUserSerializer, UserSerializer, ChangeUserPasswordSerializer,
                                ChangeUserInformationSerializer, LoginSerializer, LogoutSerializer,
                                UserDetailSerializer)
from users.models import User, ACTIVE, DEACTIVE
from rest_framework.views import APIView
from django.utils.datetime_safe import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        users = User.objects.all().order_by('-created_time')
        if users:
            serializer = UserSerializer(users, many=True)
            data = {
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                    "success":True
                }
            return Response(data=data)
        else:
            data = {
                    "data": [],
                    "status": status.HTTP_200_OK,
                    "success":True,
                    "message":"Ma'lumot mavjud emas!"
                }
            return Response(data=data)


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateUserSerializer


class ChangeUserInformationView(UpdateAPIView):
     permission_classes = (IsAuthenticated, )
     serializer_class = ChangeUserInformationSerializer
     http_method_names = ['patch', 'put']

     def get_object(self):
         return self.request.user

     def update(self, request, *args, **kwargs):
         super(ChangeUserInformationView, self).update(request, *args, **kwargs)
         data = {
             'success': True,
             'message': "User muvaffaqiyatli o'zgartirildi!"
         }
         return Response(data, status=200)

     def partial_update(self, request, *args, **kwargs):
         super(ChangeUserInformationView, self).partial_update(
             request, *args, **kwargs)
         data = {
             'success': True,
             'message': "User muvaffaqiyatli o'zgartirildi!"
         }
         return Response(data, status=200)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "success": True,
                "message": "You are loggout out"
            }
            return Response(data, status=205)
        except TokenError:
            return Response({"detail": "Token is invalid or expired"}, status=400)


class UserRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)
    
    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(instance=user, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    @swagger_auto_schema(request_body=ChangeUserPasswordSerializer)
    def patch(self, request, id):
        user = User.objects.get(id=id)
        serializer = ChangeUserPasswordSerializer(instance=user, data = request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
