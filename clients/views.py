from django.shortcuts import get_object_or_404
from clients.serializers import ClientSerializer, FileSerializer, ClientCreateSerializer, ClientUpdateCreateSerializer, GraphicSerializer
from clients.models import Client, File
from investor.models import Investor
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination


class ClientListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=ClientCreateSerializer)
    def post(self, request):
        serializer = ClientCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        else:
            data = {
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)

    def get(self, request):
        clients = Client.objects.all().order_by('-created_time')
        if clients:
            paginator = PageNumberPagination()
            page_obj = paginator.paginate_queryset(clients, request)
            serializer = ClientSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            data = {
                "data": [],
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Ma'lumot mavjud emas!"
            }
            return Response(data=data)


class ClientDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        client = get_object_or_404(Client, id=id)
        if client:
            serializer = ClientSerializer(client)
            data = {
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success": True
            }
            return Response(data=data)

    def delete(self, request, id):
        client = get_object_or_404(Client, id=id)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=ClientUpdateCreateSerializer)
    def patch(self, request, id):
        client = get_object_or_404(Client, id=id)
        serializer = ClientUpdateCreateSerializer(
            instance=client, data=request.data, partial=True)

        if serializer.is_valid():
            investor = get_object_or_404(
                Investor, id=serializer.validated_data.get('investor_id'))
                
            loan_amount = serializer.validated_data.get('loan_amount')
            if not loan_amount:
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Loan amount is required!"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            if investor.get_balance() >= loan_amount:
                serializer.save(user=request.user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                data = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Invstorda bunday mablag' mavjud emas!"
                }
                return Response(data=data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientFileAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        file = get_object_or_404(File, client__id=id)
        serializer = FileSerializer(file)
        data = {
            "data": serializer.data,
            "status": status.HTTP_200_OK,
            "success": True
        }
        return Response(data=data)


class GraphicListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        client = get_object_or_404(Client, id=id)
        graphics = client.graphics.all().order_by('id')
        if graphics:
            serializer = GraphicSerializer(graphics, many=True)
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        else:
            data = {
                "data": [],
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Ma'lumot mavjud emas!"
            }
            return Response(data=data)
