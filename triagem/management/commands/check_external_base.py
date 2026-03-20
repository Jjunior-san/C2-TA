from django.core.management.base import BaseCommand

from triagem.sync_service import healthcheck_erp


class Command(BaseCommand):
    help = 'Testa comunicação externa do C2-TA.'

    def handle(self, *args, **options):
        result = healthcheck_erp()
        if result.get('ok'):
            self.stdout.write(self.style.SUCCESS('Comunicação externa OK.'))
        else:
            self.stdout.write(self.style.ERROR(result.get('error', 'Falha desconhecida.')))
