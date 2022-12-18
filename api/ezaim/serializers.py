from rest_framework import serializers

from ezaim.models import (
    User, TelegramUser, UserSettings,
    PassportData, Address,
    PaymentCard, Payment, Loan, 
    Currency, Log
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        read_only_fields = ['id']
        fields = read_only_fields + ['name', 'full_name', 'literal']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['id']
        fields = read_only_fields + ['email', 'phone_number', 'salary', 'name', 'surname']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PassportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportData
        fields = '__all__'

class UserSettingsSerializer(serializers.ModelSerializer):
    # preferred_currency = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Currency.objects.all()
    # )

    class Meta:
        model = UserSettings
        read_only_fields = ['user']
        fields = read_only_fields + ['date_format', 'week_start', 'preferred_currency']

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        read_only_fields = ['chat_id', 'user', 'name']
        fields = read_only_fields + ['confirmed']

# todo: delete
class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        read_only_fields = ['user', 'created_at']
        fields = read_only_fields + ['percent', 'amount', 'currency', 'remaining_amount']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        read_only_fields = ['log', 'created_at']
        fields = read_only_fields

