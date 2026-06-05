from django.db import models


class SearchHistory(models.Model):
    """Stores guest searches made from the WeatherSense web UI."""

    # city or "lat,lon"
    query = models.CharField(max_length=200)
    # 'city' or 'coords'
    query_type = models.CharField(max_length=20)

    # OpenWeather derived fields
    result_city = models.CharField(max_length=100, blank=True, default="")
    result_country = models.CharField(max_length=10, blank=True, default="")
    temperature = models.FloatField(null=True, blank=True)
    condition = models.CharField(max_length=100, blank=True, default="")

    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["query_type"]),
            models.Index(fields=["timestamp"]),
        ]
        ordering = ["-timestamp"]

