from django.db import models

from .models import CitizenRecord


class CitizenProfileExtension(models.Model):
    citizen = models.OneToOneField(
        CitizenRecord,
        on_delete=models.CASCADE,
        related_name='profile_extension',
    )
    social_name = models.CharField(max_length=180, blank=True)
    mother_name = models.CharField(max_length=160, blank=True)
    neighborhood = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True, default='Amargosa')
    erp_citizen_id = models.CharField(max_length=80, blank=True)
    external_reference = models.CharField(max_length=80, blank=True)
    sync_status = models.CharField(max_length=20, default='local')
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Extensão do cidadão'
        verbose_name_plural = 'Extensões do cidadão'

    def __str__(self):
        return self.citizen.full_name
