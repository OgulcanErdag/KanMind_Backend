from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ResgistrationView, CustomLoginView, EmailCheckView

urlpatterns = [
    path('registration/', ResgistrationView.as_view(), name="registration"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]
