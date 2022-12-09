from django.db import models

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
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return self.email

class Address(BaseDbModel):
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    code_soato = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    flat = models.CharField(max_length=255)
    mail_index = models.CharField(max_length=255)

class PasportData(BaseDbModel):
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    sex = models.CharField(max_length=16)
    resident = models.CharField(max_length=255)
    birth_date = models.DateField()
    birth_place = models.ForeignKey(
        Address, 
        on_delete=models.RESTRICT,
        related_name='birth_place'
    )
    registration_address = models.ForeignKey(
        Address, 
        on_delete=models.RESTRICT,
        related_name='registration_address'
    )
    residence_place = models.ForeignKey(
        Address,
        on_delete=models.RESTRICT,
        related_name='residence_place'
    )
    nationality = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=128)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    authority = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.surname} {self.name}'

class UserSettings(BaseDbModel):
    user_id = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    date_format = models.CharField(max_length=32, default="DD/MM/YYYY")
    preferred_currency = models.ForeignKey(
        Currency, 
        on_delete=models.RESTRICT
    )
    week_start = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user_id} settings"

    class Meta:
        verbose_name_plural = "User settings"

class TelegramUser(BaseDbModel):
    chat_id = models.IntegerField()
    confirmed = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"chat#{self.chat_id}"

class PaymentCard(BaseDbModel):
    number = models.CharField(max_length=255)
    csv = models.CharField(max_length=255)
    initials = models.CharField(max_length=255)
    valid_through = models.DateField()    
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"card#{self.number}"

class Loan(BaseDbModel):
    percent = models.DecimalField(max_digits=7, decimal_places=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency_id = models.ForeignKey(Currency, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return f"Loan of {self.payment_amount}, {self.percent}%"

class Payment(BaseDbModel):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.amount} credited for {self.loan_id}"

class Log(BaseDbModel):
    log = models.TextField()

    def __str__(self) -> str:
        return f"{self.created_at}: {self.log}"