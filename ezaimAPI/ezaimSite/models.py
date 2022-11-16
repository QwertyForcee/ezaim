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

class Day(BaseDbModel):
    day = models.CharField(max_length=32)
    
    def __str__(self) -> str:
        return self.day

class DateFormat(BaseDbModel):
    date_format = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.date_format

class User(BaseDbModel):
    email = models.EmailField()
    password = models.CharField(max_length=32)
    phone_number = models.BigIntegerField()
    salary = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return self.email

class UserSettings(BaseDbModel):
    user_id = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    date_format = models.ForeignKey(DateFormat, on_delete=models.RESTRICT)
    preferred_currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)
    week_start = models.ForeignKey(Day, on_delete=models.RESTRICT)

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
    number = models.BigIntegerField()
    initials = models.CharField(max_length=255)
    valid_through = models.DateField()    
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"card#{self.number}"

class Loan(BaseDbModel):
    # created_at = models.DateTimeField(auto_now_add=True)
    percent = models.DecimalField(max_digits=7, decimal_places=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency_id = models.ForeignKey(Currency, on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return f"Loan of {self.payment_amount}, {self.percent}%"

class Payment(BaseDbModel):
    # created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.amount} credited for {self.loan_id}"

class Log(BaseDbModel):
    # created_at = models.DateTimeField(auto_now_add=True)
    log = models.TextField()

    def __str__(self) -> str:
        return f"{self.created_at}: {self.log}"

