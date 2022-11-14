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

# class Day(BaseDbModel):
#     day = models.CharField(max_length=32)

class User(BaseDbModel):
    email = models.EmailField()
    phone_number = models.BigIntegerField()
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    preferred_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    # preferred_first_day = models.ForeignKey(Day, on_delete=models.RESTRICT)
    # settings = models.JSONField()

class TelegramUser(BaseDbModel):
    chat_id = models.IntegerField()
    confirmed = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PaymentCard(BaseDbModel):
    number = models.BigIntegerField()
    initials = models.CharField(max_length=255)
    valid_through = models.DateField()    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Loan(BaseDbModel):
    # created_at = models.DateTimeField(auto_now_add=True)
    percent = models.DecimalField(max_digits=6, decimal_places=3)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency_id = models.ForeignKey(Currency, on_delete=models.RESTRICT)

class Payment(BaseDbModel):
    # created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)

class Logs(BaseDbModel):
    # created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

