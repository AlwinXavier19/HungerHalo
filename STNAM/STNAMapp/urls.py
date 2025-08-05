from django.urls import path
from .views import RegisterView, LoginView,LogoutView,RefreshTokenView,DashboardView,UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', RefreshTokenView.as_view()),
    path('me/', UserDetailView.as_view()),
    path('dashboard/', DashboardView.as_view()),
]
