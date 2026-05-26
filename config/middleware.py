"""Middleware for host-based routing."""

from django.conf import settings


class LabSiteMiddleware:
    """Route configured lab hosts to the lab URLconf.

    This allows the lab site to live on a separate subhost, such as
    lab.example.com, while the main careers site keeps using the default
    project URLconf.
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