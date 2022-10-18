from django.forms import ValidationError


def validate_2_decimal_places(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            f"{value} is in a wrong format"
        )