from rest_framework import serializers

from loans.models import (
    Currency,
    PercentOffer,
    PaymentCard,
    Loan,
    Payment
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        read_only_fields = ['id']
        fields = read_only_fields + ['name', 'full_name', 'literal']


# todo: delete
class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        read_only_fields = ['id', 'user', 'created_at', 'percent', 'remaining_amount', 'is_active']
        fields = read_only_fields + ['amount', 'currency', ]


class NewLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['amount', 'currency']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
