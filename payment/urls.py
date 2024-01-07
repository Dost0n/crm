from django.urls import path
from payment.views import PaymentAPIView, PaymentDetailAPIView


urlpatterns = [
    path('', PaymentAPIView.as_view()),
    path('<int:id>/', PaymentDetailAPIView.as_view()),
]
