from django.db import models
from simple_history.models import HistoricalRecords
class IncidentCategory(models.Model):
 name=models.CharField(max_length=120,unique=True); code=models.CharField(max_length=40,unique=True); is_active=models.BooleanField(default=True); description=models.TextField(blank=True); history=HistoricalRecords()
 def __str__(self): return self.name
