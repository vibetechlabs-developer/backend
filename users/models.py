from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("AGENT", "Agent"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="AGENT"
    )

    preferred_insurance_types = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma separated values like HOME,AUTO,LIFE"
    )

    def __str__(self):
        return self.username