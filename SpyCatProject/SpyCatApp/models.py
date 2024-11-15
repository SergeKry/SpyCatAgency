from django.db import models
from django.core.exceptions import ValidationError


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.IntegerField
    breed = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class Mission(models.Model):
    cat = models.ForeignKey(SpyCat, on_delete=models.CASCADE, related_name='missions', null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission for {self.cat.name}"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Target: {self.name}"