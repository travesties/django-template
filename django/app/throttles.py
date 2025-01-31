from rest_framework.throttling import UserRateThrottle


class BurstUserRateThrottle(UserRateThrottle):
    scope = "burst"
    rate = "60/min"