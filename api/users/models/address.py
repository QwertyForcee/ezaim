from django.db import models
from encrypted_model_fields.fields import (
    EncryptedCharField
)
from users.models import BaseDbModel

class Address(BaseDbModel):
    country = EncryptedCharField(max_length=255)
    state = EncryptedCharField(max_length=255)
    city = EncryptedCharField(max_length=255)
    code_soato = EncryptedCharField(max_length=255)
    street = EncryptedCharField(max_length=255)
    house = EncryptedCharField(max_length=255)
    flat = EncryptedCharField(max_length=255)
    mail_index = EncryptedCharField(max_length=255)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f'{self.country}, {self.state}, {self.city}'
