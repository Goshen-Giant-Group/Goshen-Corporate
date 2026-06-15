"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from urllib.parse import urljoin

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.http import HttpResponsePermanentRedirect
from django.views import View
from jobs import views as jobs_views


class OldLabPathRedirectView(View):
    """Redirect the retired lab path to the lab subhost."""

    permanent = True

    def get(self, request, *args, **kwargs):
        target_base = settings.LAB_CANONICAL_URL or '/'
        target_url = urljoin(target_base, '/')
        return HttpResponsePermanentRedirect(target_url)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Goshen Corporate (Jobs/Careers)
    path('', jobs_views.careers, name='home'),
    path('about/', jobs_views.about, name='about'),
    path('contact/', jobs_views.contact, name='contact'),
    path('careers/', jobs_views.careers, name='careers'),
    path('careers/jobs/<int:pk>/', jobs_views.job_detail, name='job_detail'),
    path('careers/apply/general/', jobs_views.general_application, name='general_application'),
    path('careers/jobs/<int:pk>/apply/', jobs_views.job_application, name='job_application'),
    path('lab/', include(('lab.urls', 'lab'), namespace='lab')),

    # Retired lab path: redirect to the subhost.
    path('naturis-analytical-lab/', OldLabPathRedirectView.as_view()),
]
