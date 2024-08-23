from django.core.cache import cache
from django.utils import timezone


class CustomRateLimit:
    def __init__(self, rate_limit, time_period):
        self.rate_limit = rate_limit
        self.time_period = time_period

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def is_rate_limited(self, request):
        client_ip = self.get_client_ip(request)
        cache_key = f"rl:{client_ip}"
        request_times = cache.get(cache_key, [])

        # Remove old requests that are outside the time period
        request_times = [
            t for t in request_times if t > timezone.now() - self.time_period
        ]

        if len(request_times) >= self.rate_limit:
            return True

        request_times.append(timezone.now())
        cache.set(cache_key, request_times, self.time_period.total_seconds())
        return False
