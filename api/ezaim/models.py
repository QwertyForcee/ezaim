from django.db import models
from encrypted_model_fields.fields import EncryptedCharField, EncryptedBooleanField, EncryptedDateTimeField
from datetime import datetime
from dateutil import relativedelta
import pytz

utc = pytz.UTC

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
        return self.name

    class Meta:
        verbose_name_plural = "Currencies"

class PercentOffer(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    percent = models.DecimalField(max_digits=7, decimal_places=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.percent*100}% for < {self.amount}{self.currency.literal}'

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
    # number = EncryptedCharField(max_length=255)
    # csv = EncryptedCharField(max_length=255)
    # initials = EncryptedCharField(max_length=255)
    # valid_through = EncryptedDateTimeField() # test this
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = EncryptedCharField(max_length=255)

    def __str__(self) -> str:
        return f"card owned by {self.user}"

class AuthUpdateLoanQuerySet(models.query.QuerySet):
    def get(self, **kwargs):
        loan: Loan = super().get(**kwargs)
        today = utc.localize(datetime.fromisocalendar(2023, 10, 1))
        delta = relativedelta.relativedelta(today, loan.created_at)
        months_passed = delta.years * 12 + delta.months
        if months_passed > loan.months_passed:
            if loan.remaining_amount > 0:
                months_diff = months_passed - loan.months_passed
                loan.remaining_amount += loan.amount * loan.percent * months_diff
            loan.months_passed = months_passed
            loan.save()
        return super().get(**kwargs)

class AutoUpdateLoanManager(models.Manager.from_queryset(AuthUpdateLoanQuerySet)):
    pass

class Loan(BaseDbModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    percent = models.DecimalField(max_digits=7, decimal_places=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2)
    months_passed = models.IntegerField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)

    objects = AutoUpdateLoanManager()
    def __str__(self) -> str:
        return f"Loan of {self.amount} {self.currency}, {self.percent}%"

class Payment(BaseDbModel):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.amount} credited for {self.loan}"

class OrderUser(BaseDbModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user}, order #{self.pk}'


class Log(BaseDbModel):
    log = models.TextField()

    def __str__(self) -> str:
        return f"{self.created_at}: {self.log}"
