from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, "CANONICAL_HOST", None)
        if canonical_host:
            request_host = request.get_host().split(":")[0].lower()
            redirect_hosts = {
                host.lower()
                for host in getattr(settings, "CANONICAL_HOST_REDIRECTS", [])
            }

            if request_host in redirect_hosts:
                scheme = getattr(settings, "CANONICAL_SCHEME", "https")
                return HttpResponsePermanentRedirect(
                    f"{scheme}://{canonical_host}{request.get_full_path()}"
                )

        return self.get_response(request)
