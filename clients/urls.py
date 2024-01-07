from django.urls import path
from clients.views import (ClientListCreateAPIView, ClientDetailAPIView, ClientFileAPIView, GraphicListAPIView)
from payment.views import ClientPaymentsAPIView

urlpatterns = [
    path('', ClientListCreateAPIView.as_view()),
    path('<int:id>/', ClientDetailAPIView.as_view()),
    path('<int:id>/file/', ClientFileAPIView.as_view()),
    path('<int:id>/graphics/', GraphicListAPIView.as_view()),
    path('<int:id>/payments/', ClientPaymentsAPIView.as_view()),
]
