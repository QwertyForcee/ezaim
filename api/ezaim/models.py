from django.db import models
from encrypted_model_fields.fields import EncryptedCharField

class BaseDbModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Currency(BaseDbModel):
    name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=64)
    literal = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name_plural = "Currencies"

class User(BaseDbModel):
    email = models.EmailField()
    password = models.BinaryField()
    salt = models.BinaryField()
    phone_number = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.email

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

class PassportData(BaseDbModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    name = EncryptedCharField(max_length=255)
    surname = EncryptedCharField(max_length=255)
    sex = EncryptedCharField(max_length=255)
    resident = EncryptedCharField(max_length=255)
    birth_date = EncryptedCharField(max_length=255)
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
    issue_date = EncryptedCharField(max_length=255)
    expiry_date = EncryptedCharField(max_length=255)
    authority = EncryptedCharField(max_length=255)

    def __str__(self) -> str:
        return f'Passport data, user: {self.user}'

    class Meta:
        verbose_name_plural = "Passports' data"

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

class TelegramUser(BaseDbModel):
    chat_id = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}#{self.chat_id}"

class PaymentCard(BaseDbModel):
    number = models.CharField(max_length=255)
    csv = models.CharField(max_length=255)
    initials = models.CharField(max_length=255)
    valid_through = models.DateField()    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"card owned by {self.user}"

class Loan(BaseDbModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    percent = models.DecimalField(max_digits=7, decimal_places=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return f"Loan of {self.amount}, {self.percent}%"

class Payment(BaseDbModel):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.amount} credited for {self.loan}"

class Log(BaseDbModel):
    log = models.TextField()

    def __str__(self) -> str:
        return f"{self.created_at}: {self.log}"
