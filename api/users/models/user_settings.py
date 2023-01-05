from django.db import models
from users.models import BaseDbModel, User
from loans.models import Currency

class UserSettings(BaseDbModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    date_format = models.CharField(max_length=32, default="MM/DD/YYYY")
    preferred_currency = models.ForeignKey(
        Currency, 
        on_delete=models.RESTRICT,
        null=True
    )
    week_start = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} settings"

    class Meta:
        verbose_name_plural = "User settings"
