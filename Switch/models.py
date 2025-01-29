from django.db import models
from django.db.models import UniqueConstraint, Q

# Create your models here.

PRODUCTION_SWITCH = (
    ('locked', 'Locked'),
    ('production', 'Production'),
    ('testing', 'Testing'),
)

class ProductionSwitch(models.Model):
    production_switch = models.CharField(choices=PRODUCTION_SWITCH, max_length=15, default='locked')
    contsraint = models.IntegerField(primary_key=True, default=1, editable=False)

    class Meta:
        verbose_name_plural = 'Production Switch'
        constraints = [
            UniqueConstraint(fields=['contsraint'], condition=Q(contsraint=1), name='only_one_production_switch'),
        ]
        managed = True

    def __str__(self):
        return 'Production Switch'