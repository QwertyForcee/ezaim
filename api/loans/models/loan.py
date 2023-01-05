from django.db import models
from datetime import datetime
from dateutil import relativedelta
import pytz

from loans.models import BaseDbModel, Currency
from users.models import User

utc = pytz.UTC

class AuthUpdateLoanQuerySet(models.query.QuerySet):
    def get(self, **kwargs):
        loan: Loan = super().get(**kwargs)

        if loan.remaining_amount <= 0:
            loan.is_active = False
            loan.save()

        if not loan.is_active:
            return super().get(**kwargs)

        # if months passed and loan active increase loan
        today = utc.localize(datetime.today())
        delta = relativedelta.relativedelta(today, loan.created_at)
        months_passed = delta.years * 12 + delta.months
        if months_passed > loan.months_passed:
            months_diff = months_passed - loan.months_passed
            loan.remaining_amount += loan.amount * loan.percent * months_diff
            loan.months_passed = months_passed
            loan.save()
        
        return super().get(**kwargs)

class AutoUpdateLoanManager(models.Manager.from_queryset(AuthUpdateLoanQuerySet)):
    pass

class Loan(BaseDbModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    percent = models.DecimalField(max_digits=7, decimal_places=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2)
    months_passed = models.IntegerField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)

    objects = AutoUpdateLoanManager()
    def __str__(self) -> str:
        return f"Lend out: {self.amount} {self.currency}; {self.percent*100:.1f}% monthly; Remaining to pay:{self.remaining_amount}"
