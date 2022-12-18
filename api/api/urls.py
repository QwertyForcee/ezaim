from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api import settings
from ezaim.views import (
    not_found, app_error,
    login, signup,
    UserViewSet,
    UserSettingsViewSet,
    TelegramUsersViewSet,
    CurrencyViewSet,
    LoanViewSet,
    PaymentViewSet,
    PaymentCardViewSet
)
from ezaim.views import test_pay, test_loan


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
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
router.register(r'telegram-users', TelegramUsersViewSet, basename='telegram-users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/login', login),
    path('api/v1/auth/signup', signup),
    path('pay/', test_pay),
    path('loan/', test_loan),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger-ui/$', schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
                name='schema-redoc'),
    ]
