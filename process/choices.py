from django.db import models

class StatusChoices(models.TextChoices):
    PENDING = 'PENDING', 'Pendiente'
    PROCESSING = 'PROCESSING', 'En proceso'
    COMPLETE = 'COMPLETE', 'Completado'
    ERROR = 'ERROR', 'Error'