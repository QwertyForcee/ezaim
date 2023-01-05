from django.db import models
from loans.models import Currency

class PercentOffer(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    percent = models.DecimalField(max_digits=7, decimal_places=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.percent*100:.1f}% for < {self.amount}{self.currency.literal}'
