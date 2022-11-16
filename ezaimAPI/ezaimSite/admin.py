from django.contrib import admin
from .models import (
    User, TelegramUser, UserSettings,
    PaymentCard, Payment, Loan, 
    Currency, Day, DateFormat, Log
)

# Register your models here.

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

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    pass

@admin.register(DateFormat)
class DateFormatAdmin(admin.ModelAdmin):
    pass
