from django.contrib import admin
from django.urls import path

from users.custom_jwt_claims import CustomTokenObtainPairView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
