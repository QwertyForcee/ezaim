from django.db import models
from users.models import BaseDbModel

class User(BaseDbModel):
    email = models.EmailField()
    password = models.BinaryField()
    salt = models.BinaryField()
    phone_number = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def is_authenticated():
        return True

    def __str__(self) -> str:
        return self.email