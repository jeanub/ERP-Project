from django.db import models
from core.models import TimeStampedModel
class Customer(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self): return self.name
