from investor.serializers import InvestorDetailSerializer, InvestorSerializer, InvestmentSerializer, InvestmentDetailSerializer
from investor.models import Investor, Investment
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from config.custom_pagination import CustomPagination
from django.db.models import Sum, Q


class InvestorAPIView(APIView, CustomPagination):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=InvestorDetailSerializer)
    def post(self, request):
        serializer = InvestorSerializer(data=request.data)
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
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Ma'lumot yuborishda xatolik"
            }
            return Response(data=data)

    def get(self, request):
        balance = Sum('investments__amount', filter=Q(investments__is_credit=True), default=0) - \
            Sum('investments__amount', filter=Q(investments__is_credit=False), default=0)
        consumption = Sum('investments__amount', filter=Q(
            investments__type=3), default=0)
        coming = Sum('investments__amount', filter=Q(
            investments__type=4), default=0)
        remainder = Sum('clients__loan_amount', default=0)
        expected_income = Sum('clients__income_amount', default=0)
        real_income = Sum('clients__real_income', default=0)

        entity = Investor.objects.annotate(
            balance=balance,
            consumption=consumption,
            coming=coming,
            remainder=remainder,
            expected_income=expected_income,
            real_income=real_income
        ).order_by('-created_time')

        results = self.paginate_queryset(entity, request, view=self)
        serializer = InvestorSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class InvestorDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        refill = Sum('investments__amount', filter=Q(
            investments__type=1), default=0)
        withdraw = Sum('investments__amount', filter=Q(
            investments__type=2), default=0)
        balance = Sum('investments__amount', filter=Q(investments__is_credit=True), default=0) - \
            Sum('investments__amount', filter=Q(investments__is_credit=False), default=0)
        consumption = Sum('investments__amount', filter=Q(
            investments__type=3), default=0)
        coming = Sum('investments__amount', filter=Q(
            investments__type=4), default=0)
        remainder = Sum('clients__loan_amount', default=0)
        expected_income = Sum('clients__income_amount', default=0)
        real_income = Sum('clients__real_income', default=0)
        try:
            investor = Investor.objects.annotate(
                balance=balance,
                refill=refill,
                withdraw=withdraw,
                expected_income=expected_income,
                real_income=real_income,
                consumption=consumption,
                coming=coming,
                remainder=remainder
            ).filter(id=id)
        except Exception as e:
            data = {
                "message": "Noto'g'ri ID kiritildi.",
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not investor.exists():
            data = {
                "message": "Ma'lumot topilmadi.",
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        serializer = InvestorDetailSerializer(investor.first())
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=InvestorSerializer)
    def patch(self, request, id):
        investor = get_object_or_404(Investor, id=id)
        serializer = InvestorSerializer(
            investor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        investor = get_object_or_404(Investor, id=id)
        investor.delete()
        data = {
            "message": "Ma'lumot muvaffaqiyatli o'chirildi.",
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class InvesmentAPIView(APIView, CustomPagination):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        entity = Investment.objects.all().order_by('-created_time')
        results = self.paginate_queryset(entity, request, view=self)
        serializer = InvestmentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=InvestmentDetailSerializer)
    def post(self, request):
        serializer = InvestmentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            data = {
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Ma'lumot muvaffaqiyatli qo'shildi."
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "error": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Ma'lumot yuborishda xatolik"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class InvestmentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        investment = get_object_or_404(Investment, id=id)
        serializer = InvestmentSerializer(investment)
        return Response(data=serializer.data)
