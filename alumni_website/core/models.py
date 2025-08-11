from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
class RecommendationSystem(models.Model):

    UNOPTIMISED = "UnoptimisedAlgorithm"
    OPTIMIZED = "OptimisedAlgorithm"
    SIMPLE = "SimpleAlgorithm"
    ALGORITHM_CHOICES = [
        (OPTIMIZED, "OptimisedAlgorithm"),
        (SIMPLE, "SimpleAlgorithm"),
        (UNOPTIMISED, "UnoptimisedAlgorithm")
    ]


    recommendation_system = models.CharField(
        max_length=200,
        choices=ALGORITHM_CHOICES,
        default=SIMPLE,
    )

    def __str__(self):
        return self.recommendation_system
