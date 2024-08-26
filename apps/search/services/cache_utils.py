from functools import wraps

from django.core.cache import cache


def cache_queryset(timeout=60):
    def decorator(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            """
            TODO: Remove cache_key when there is changes in Employee model
            """
            if not self.request.user.organizations.exists():
                return func(self, *args, **kwargs)

            cache_key = (
                f"{self.__class__.__name__}_{self.request.user.id}_"
                f"{self.request.user.organizations.first().id}_{self.request.query_params.urlencode()}"
            )
            cached_queryset = cache.get(cache_key)
            if cached_queryset is not None:
                return cached_queryset

            queryset = func(self, *args, **kwargs)
            cache.set(cache_key, queryset, timeout=timeout)
            return queryset

        return wrapped

    return decorator
