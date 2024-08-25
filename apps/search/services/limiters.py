from datetime import timedelta
from functools import wraps

from django.core.cache import cache
from django.utils import timezone
from rest_framework.response import Response


def rate_limit(rate_limit_class, rate_limit_request: int, time_period: timedelta):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            rate_limiter = rate_limit_class(rate_limit_request, time_period)

            if rate_limiter.is_rate_limited(request):
                return Response(
                    {"detail": "Rate limit exceeded. Try again later."}, status=429
                )

            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    return decorator


class CustomRateLimit:
    def __init__(self, rate_limit, time_period):
        self.rate_limit = rate_limit
        self.time_period = time_period

    def get_client_ip(self, request):
        """Get the client's IP address from request header"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def is_rate_limited(self, request):
        """Check if rate limit is exceeded"""
        client_ip = self.get_client_ip(request)
        cache_key = f"rl:{client_ip}"
        request_times = cache.get(cache_key, [])

        request_times = [
            t for t in request_times if t > timezone.now() - self.time_period
        ]

        if len(request_times) >= self.rate_limit:
            return True

        request_times.append(timezone.now())
        cache.set(cache_key, request_times, self.time_period.total_seconds())
        return False
