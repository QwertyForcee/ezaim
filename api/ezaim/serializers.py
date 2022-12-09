from rest_framework import serializers

from ezaim.models import (
    User, TelegramUser, UserSettings,
    PaymentCard, Payment, Loan, 
    Currency, Log
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['id']
        fields = read_only_fields + ['email', 'phone_number', 'salary']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        read_only_fields = ['id']
        fields = read_only_fields + ['name', 'full_name', 'literal']

class UserSettingsSerializer(serializers.ModelSerializer):
    preferred_currency = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Currency.objects.all()
    )

    class Meta:
        model = UserSettings
        read_only_fields = ['user_id']
        fields = read_only_fields + ['date_format', 'week_start', 'preferred_currency']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = '__all__'


