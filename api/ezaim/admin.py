from django.contrib import admin
from ezaim.models import (
    User, TelegramUser, UserSettings,
    PaymentCard, Payment, Loan, 
    Currency, Log
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    pass

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass
