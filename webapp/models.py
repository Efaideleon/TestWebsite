from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, default='', null=True)
    def __str__(self):
        return self.name

class dataMCU(models.Model):
    soil_moisture = models.IntegerField(default=0)
    soil_temp = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    class Meta:
        managed = True
        db_table = 'dataMCU'
