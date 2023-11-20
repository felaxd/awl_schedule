from django.utils import timezone


def get_current_year() -> int:
    return timezone.now().year


def get_current_month() -> int:
    return timezone.now().month
