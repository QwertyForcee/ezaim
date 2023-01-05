from rest_framework import serializers

from users.models import (
    User,
    Address,
    PassportData,
    UserSettings,
    TelegramUser,
    Log
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['id']
        fields = read_only_fields + ['email', 'phone_number', 'name', 'surname', 'salary']


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


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        read_only_fields = ['log', 'created_at']
        fields = read_only_fields
