import requests

from .vendor_api import VendorAPI
from django.conf import settings

VENDOR_API_KEY = getattr(settings, "VENDOR_API_KEY")


class APIConfigurationError(Exception):
    pass


if VENDOR_API_KEY is None:
    raise APIConfigurationError("VENDOR_API_KEY must be provided")

# Sessions allow us to persist parameters across requests, such as API keys.
# They also reuse underlying TCP connections when making multiple requests
# to the same host, so this approach my have a positive performance impact.
session = requests.Session()
session.headers.update({"Vendor-API-Key": VENDOR_API_KEY})


__all__ = ["session", "VendorAPI"]
