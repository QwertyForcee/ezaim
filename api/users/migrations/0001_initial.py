# Generated by Django 4.1.3 on 2023-01-05 18:04

from django.db import migrations, models
import django.db.models.deletion
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', encrypted_model_fields.fields.EncryptedCharField()),
                ('state', encrypted_model_fields.fields.EncryptedCharField()),
                ('city', encrypted_model_fields.fields.EncryptedCharField()),
                ('code_soato', encrypted_model_fields.fields.EncryptedCharField()),
                ('street', encrypted_model_fields.fields.EncryptedCharField()),
                ('house', encrypted_model_fields.fields.EncryptedCharField()),
                ('flat', encrypted_model_fields.fields.EncryptedCharField()),
                ('mail_index', encrypted_model_fields.fields.EncryptedCharField()),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('log', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.BinaryField()),
                ('salt', models.BinaryField()),
                ('phone_number', models.CharField(max_length=255)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=15)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('date_format', models.CharField(default='MM/DD/YYYY', max_length=32)),
                ('week_start', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'User settings',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chat_id', models.IntegerField()),
                ('confirmed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PassportData',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('name', encrypted_model_fields.fields.EncryptedCharField()),
                ('surname', encrypted_model_fields.fields.EncryptedCharField()),
                ('sex', encrypted_model_fields.fields.EncryptedCharField()),
                ('resident', encrypted_model_fields.fields.EncryptedBooleanField()),
                ('birth_date', encrypted_model_fields.fields.EncryptedDateTimeField()),
                ('birth_country', encrypted_model_fields.fields.EncryptedCharField()),
                ('birth_state', encrypted_model_fields.fields.EncryptedCharField()),
                ('birth_city', encrypted_model_fields.fields.EncryptedCharField()),
                ('nationality', encrypted_model_fields.fields.EncryptedCharField()),
                ('passport_number', encrypted_model_fields.fields.EncryptedCharField()),
                ('identification_number', encrypted_model_fields.fields.EncryptedCharField()),
                ('issue_date', encrypted_model_fields.fields.EncryptedDateTimeField()),
                ('expiry_date', encrypted_model_fields.fields.EncryptedDateTimeField()),
                ('authority', encrypted_model_fields.fields.EncryptedCharField()),
                ('registration_address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='registration_address', to='users.address')),
                ('residential_address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='residential_address', to='users.address')),
            ],
            options={
                'verbose_name_plural': "Passports' data",
            },
        ),
    ]
