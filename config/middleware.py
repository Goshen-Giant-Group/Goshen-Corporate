"""Middleware for host-based routing."""

from django.conf import settings


class LabSiteMiddleware:
    """Route configured lab hosts to their respective URLconf.

    This allows:
    - lab.example.com -> lab.urls (request.lab_site = True)
    - main corporate domain -> config.urls (careers/jobs)
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.lab_hosts = {host.lower() for host in getattr(settings, 'LAB_HOSTS', [])}

    def __call__(self, request):
        host = request.get_host().split(':', 1)[0].lower()
        is_lab_site = host in self.lab_hosts
        request.lab_site = is_lab_site

        if is_lab_site:
            request.urlconf = 'lab.urls'
        return self.get_response(request)
