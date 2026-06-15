from django.conf import settings
from django.shortcuts import render


def index(request):
    """Render the static Goshen Laboratory (Naturis) index page.

    This view intentionally does not rely on any models so the app
    remains a static, easy-to-extract component of the project.
    """
    canonical_url = settings.LAB_CANONICAL_URL or request.build_absolute_uri('/')
    return render(
        request,
        'lab/index.html',
        {
            'canonical_url': canonical_url,
            'meta_description': (
                'Naturis Analytical Laboratory Services Ltd provides environmental, '
                'food, industrial, and quality assurance testing under Goshen Giant Group.'
            ),
        },
    )
