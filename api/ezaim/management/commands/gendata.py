from django.core.management.base import BaseCommand, CommandError
from ezaim.models import PercentOffer, Currency
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate initial data for database'

    def handle(self, *args, **options):
        try:
            currencies = Currency.objects.all()
            for currency in currencies:
                currency.delete()
            offers = PercentOffer.objects.all()
            for offer in offers:
                offer.delete()
        except Exception as e:
            self.stdout.write(f'error: {e}')
            return
        else:
            self.stdout.write(f'Currencies and offers deleted')

        try:
            cur = Currency(
                name = 'BYN',
                full_name = 'Belarussian Rouble',
                literal = 'Br'
            )
            cur.save()
            PercentOffer(
                currency = cur,
                percent = Decimal('0.05'),
                amount = Decimal('100')
            ).save()
            PercentOffer(
                currency = cur,
                percent = Decimal('0.01'),
                amount = Decimal('200')
            ).save()

            cur = Currency(
                name = 'USD',
                full_name = 'United Stated Dollar',
                literal = '$'
            )
            cur.save()
            PercentOffer(
                currency = cur,
                percent = Decimal('0.10'),
                amount = Decimal('100')
            ).save()
            PercentOffer(
                currency = cur,
                percent = Decimal('0.05'),
                amount = Decimal('200')
            ).save()
            
        except Exception as e:
            self.stdout(f'error: {e}')
            return
        else:
            self.stdout.write('Currencies and offers generated')

        
