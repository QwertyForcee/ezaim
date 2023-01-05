from django.db import models
from loans.models import BaseDbModel

class Currency(BaseDbModel):
    name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=64)
    literal = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Currencies"