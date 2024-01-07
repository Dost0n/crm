from django.urls import path
from investor.views import InvestorAPIView, InvestorDetailAPIView, InvesmentAPIView, InvestmentDetailAPIView


urlpatterns = [
    path('investors/', InvestorAPIView.as_view(), name='investors'),
    path('investors/<int:id>/', InvestorDetailAPIView.as_view(), name='investor'),
    path('investments/', InvesmentAPIView.as_view(), name='investments'),
    path('investments/<int:id>/', InvestmentDetailAPIView.as_view(), name='investment'),
]
