"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ezaim.views import (
    not_found, app_error,
    UserViewSet,
    UserSettingsViewSet,
    CurrencyViewSet,
    LoanViewSet,
    PaymentViewSet,
    PaymentCardViewSet
)


handler404 = not_found
handler500 = app_error

router = routers.SimpleRouter()
# router.include_root_view = False

router.register(r'users', UserViewSet, basename='users') 
router.register(r'loans', LoanViewSet, basename='loans')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'cards', PaymentCardViewSet, basename='cards')
router.register(r'user-settings', UserSettingsViewSet, basename='user-settings')
router.register(r'currencies', CurrencyViewSet, basename='currencies')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/', include(router.urls))
]
