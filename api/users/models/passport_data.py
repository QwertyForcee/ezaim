from django.db import models
from encrypted_model_fields.fields import (
    EncryptedCharField, 
    EncryptedBooleanField, 
    EncryptedDateTimeField
)
from users.models import BaseDbModel, User, Address

class PassportData(BaseDbModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    name = EncryptedCharField(max_length=255)
    surname = EncryptedCharField(max_length=255)
    sex = EncryptedCharField(max_length=255)
    resident = EncryptedBooleanField()
    birth_date = EncryptedDateTimeField(max_length=255)
    birth_country = EncryptedCharField(max_length=255)
    birth_state = EncryptedCharField(max_length=255)
    birth_city = EncryptedCharField(max_length=255)
    registration_address = models.ForeignKey(
        Address, 
        on_delete=models.RESTRICT,
        related_name='registration_address'
    )
    residential_address = models.ForeignKey(
        Address,
        on_delete=models.RESTRICT,
        related_name='residential_address'
    )
    nationality = EncryptedCharField(max_length=255)
    passport_number = EncryptedCharField(max_length=255)
    identification_number = EncryptedCharField(max_length=255)
    issue_date = EncryptedDateTimeField()
    expiry_date = EncryptedDateTimeField()
    authority = EncryptedCharField(max_length=255)

    def __str__(self) -> str:
        return f'Passport data, user: {self.user}'

    class Meta:
        verbose_name_plural = "Passports' data"
