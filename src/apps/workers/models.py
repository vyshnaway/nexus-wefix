from django.db import models
from django.conf import settings

class WorkerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='worker_profile')
    skills = models.JSONField(default=list)  # ["plumbing", "carpentry"]
    location = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.JSONField(default=dict)  # Schedule

    def __str__(self):
        return f"{self.user.email} - {self.location}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
