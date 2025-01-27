from . import session


class VendorAPI:
    """
    Wrapper class for vendor API.
    """

    def example_get(self) -> dict[str, str]:
        response = session.get("add real api url")
        response.raise_for_status()
        return response.json()
