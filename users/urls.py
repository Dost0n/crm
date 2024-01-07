from django.urls import path
from users.views import (CreateUserView, UserPasswordChangeAPIView, ChangeUserInformationView, UserRetrieveUpdateDeleteAPIView,
                            LoginView, LogoutView, UserListAPIView, UserDetailAPIView)


urlpatterns = [
    path('profile/', UserDetailAPIView.as_view()),
    path('list/', UserListAPIView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('update/', ChangeUserInformationView.as_view()),
    path('<int:id>/', UserRetrieveUpdateDeleteAPIView.as_view()),
    path('<int:id>/change_password/', UserPasswordChangeAPIView.as_view()),
]
