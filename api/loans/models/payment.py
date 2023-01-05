from django.db import models
from loans.models import BaseDbModel, Loan

class Payment(BaseDbModel):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.amount} {self.loan.currency} payed for loan#{self.loan.pk}"
