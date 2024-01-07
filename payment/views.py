from payment.serializers import PaymentSerializer, PaymentCreateSerializer
from payment.models import Payment
from clients.models import Graphic, Client
from investor.models import Investment, Investor
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from config.custom_pagination import CustomPagination


def change_client_graphics(client_id, amount):
    client = get_object_or_404(Client, id=client_id)
    graphics = Graphic.objects.filter(client=client).exclude(paid_amount=client.current_debit).order_by('id')
    for graphic in graphics:
        if graphic.remaining_amount-amount>0:
            graphic.paid_amount=amount
            graphic.remaining_amount=graphic.remaining_amount-amount
            graphic.save()
            amount=0
        if graphic.remaining_amount-amount==0:
            graphic.paid_amount=amount
            graphic.remaining_amount=0
            graphic.save()
            amount=0
        if graphic.remaining_amount-amount<0:
            graphic.paid_amount=graphic.amount
            amount=amount-graphic.remaining_amount
            graphic.remaining_amount=0
            graphic.save()


class PaymentAPIView(APIView, CustomPagination):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=PaymentCreateSerializer)
    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            investor = Investor.objects.get(
                clients__id=serializer.validated_data['client_id'])
            investment = Investment.objects.create(
                investor=investor,
                amount=serializer.validated_data['amount'],
                type=4,
                date=serializer.validated_data.get('date'),
                user=request.user,
                comment="Оплата долга")
            serializer.save(user=request.user, transaction=investment.transaction)
            client_id = serializer.validated_data['client_id']
            amount = serializer.validated_data['amount']
            change_client_graphics(client_id, amount)
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data)
        else:
            data = {
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)

    def get(self, request):
        entity = Payment.objects.all().order_by('-created_time')
        results = self.paginate_queryset(entity, request, view=self)
        serializer = PaymentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class PaymentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        investor = get_object_or_404(Payment, id=id)
        serializer = PaymentSerializer(investor)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def patch(self, request, id):
        payment = get_object_or_404(Payment, id=id)
        serializer = PaymentSerializer(
            payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        payment = get_object_or_404(Payment, id=id)
        payment.delete()
        data = {
            "message": "Ma'lumot muvaffaqiyatli o'chirildi.",
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class ClientPaymentsAPIView(APIView, CustomPagination):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        entity = Payment.objects.filter(client_id=id).order_by('-created_time')
        results = self.paginate_queryset(entity, request, view=self)
        serializer = PaymentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)