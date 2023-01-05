from django.contrib import admin

from loans.models import (
    Currency,
    PercentOffer,
    PaymentCard,
    Loan,
    Payment
)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(PercentOffer)
class PercentOfferAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    pass


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
