class SessionAPI:
    """
    Wrapper class for user session access.
    """

    def __init__(self, request):
        self.request = request

    def get_example(self):
        return self.request.session.get("example-session-key", default=[])
