from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    country = models.CharField(
        max_length=50,
        blank=True
    )  # optional extra field
    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name  # Return the name as the string representation


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    type = models.CharField(
        max_length=15,
        choices=CAR_TYPES,
        default='SUV'
    )

    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2025)
        ]
    )
    color = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name
