from django.db import models


class SensorData(models.Model):
    timestamp = models.CharField(max_length=20, unique=True)
    temperature = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    gas = models.CharField(max_length=10)
    sensor_id = models.CharField(max_length=20)

    class Meta:
        db_table = "sensor_data"

    def __str__(self):
        return f"{self.timestamp} - {self.sensor_id}"
