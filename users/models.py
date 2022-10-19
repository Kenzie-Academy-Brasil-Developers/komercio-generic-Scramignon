from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.validators import UnicodeUsernameValidator

import uuid

# Create your models here.
class User(AbstractUser):
    """
    Mutated properties
    """
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )

    username_validator = UnicodeUsernameValidator()

    username = models.TextField(
        unique=True,
        help_text="Required. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists."
        }
    )

    first_name = models.CharField("fist name", max_length=50)
    last_name = models.CharField("last name", max_length=50)

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name"
    ]

    """
    new properties
    """
    is_seller = models.BooleanField(
        default=False,
    )

