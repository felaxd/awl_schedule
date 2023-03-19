from typing import Any, Optional

from django.core import exceptions as django_exceptions

from rest_framework.views import exception_handler
from rest_framework import exceptions as rest_framework_exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response


def custom_exception_handler(exc: Any, context: Any) -> Optional[Response]:
    """
    Inspired by https://github.com/HackSoftware/Django-Styleguide#errors--exception-handling

    Handler response
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, django_exceptions.ValidationError):
        exc = rest_framework_exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, django_exceptions.ObjectDoesNotExist):
        exc = rest_framework_exceptions.NotFound()

    if isinstance(exc, django_exceptions.SuspiciousOperation):
        exc = rest_framework_exceptions.NotAcceptable

    response = exception_handler(exc, context)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    if isinstance(exc, rest_framework_exceptions.ValidationError):
        response.data["message"] = "Validation error."
        response.data["extra"] = {"fields": response.data["detail"]}  # type: ignore
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response
