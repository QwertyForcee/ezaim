from django.db import models
from encrypted_model_fields.fields import EncryptedCharField

from loans.models import BaseDbModel
from users.models import User

class PaymentCard(BaseDbModel):
    # number = EncryptedCharField(max_length=255)
    # csv = EncryptedCharField(max_length=255)
    # initials = EncryptedCharField(max_length=255)
    # valid_through = EncryptedDateTimeField() # test this
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    token = EncryptedCharField(max_length=255)

    def __str__(self) -> str:
        return f"card owned by {self.user}"