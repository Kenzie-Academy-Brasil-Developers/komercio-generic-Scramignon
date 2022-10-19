from django.db import models
from utils.validators import validate_2_decimal_places
from users.models import User

class Product(models.Model):
    description = models.TextField()
    price = models.FloatField(
        validators=[validate_2_decimal_places]
    )
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(
        default=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products"
    )