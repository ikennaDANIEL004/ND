from django.conf import settings


def canonical_url(request):
    host = getattr(settings, "CANONICAL_HOST", request.get_host().split(":")[0])
    scheme = getattr(settings, "CANONICAL_SCHEME", "https")
    return {
        "canonical_url": f"{scheme}://{host}{request.path}",
    }
