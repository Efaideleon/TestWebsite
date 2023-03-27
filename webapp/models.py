from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class dataMCU(models.Model):
    user =models.ManyToOneRel(User, on_delete=models.CASCADE, null=True)
    soil_moisture = models.IntegerField(default=0)
    soil_temp = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    class Meta:
        managed = True
        db_table = 'dataMCU'
