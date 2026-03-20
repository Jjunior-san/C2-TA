from django.core.management.base import BaseCommand

from triagem.models import AttendanceUnit, ServiceCatalog


class Command(BaseCommand):
    help = 'Cria unidade e serviços iniciais do C2-TA.'

    def handle(self, *args, **options):
        unit, _ = AttendanceUnit.objects.get_or_create(
            code='CENTRAL',
            defaults={
                'name': 'Central de Atendimento',
                'address': 'Sede administrativa',
                'phone': '',
                'email': '',
            },
        )

        default_services = [
            ('CADASTRO-GERAL', 'Cadastro geral', 10, True),
            ('INFORMACOES', 'Informações e orientação', 8, False),
            ('PROTOCOLO', 'Protocolo e recebimento', 12, True),
            ('SEGUNDA-VIA', 'Segunda via e emissão', 15, True),
        ]

        created = 0
        for code, name, estimated_minutes, requires_screening in default_services:
            _, was_created = ServiceCatalog.objects.get_or_create(
                unit=unit,
                code=code,
                defaults={
                    'name': name,
                    'description': f'Serviço inicial do C2-TA: {name}.',
                    'estimated_minutes': estimated_minutes,
                    'requires_screening': requires_screening,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS('Bootstrap do C2-TA concluído.'))
        self.stdout.write(f'Unidade base: {unit.name}')
        self.stdout.write(f'Serviços criados nesta execução: {created}')
