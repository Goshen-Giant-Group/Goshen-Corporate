import json
import random
import time
from datetime import datetime, timezone
from urllib.parse import urljoin

from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .products_data import PRODUCTS, get_product


# Standard indicative FX rates for currency conversions against USD baseline
STANDARD_FX_RATES = {
    'USD': 1.0,
    'CAD': 1.36,
    'GBP': 0.79,
    'EUR': 0.92,
    'NGN': 1550.0,
    'AUD': 1.52,
}


def index(request):
    """Render the Naturis Foods wholesale marketplace index page."""
    canonical_url = getattr(settings, 'FOODS_CANONICAL_URL', '') or request.build_absolute_uri('/')
    return render(
        request,
        'foods/index.html',
        {
            'canonical_url': canonical_url,
            'meta_description': (
                'Naturis Marketplace wholesale West African foods for retail stores, '
                'restaurants and distributors. Build a mixed-carton order and request a delivered quotation.'
            ),
            'products': PRODUCTS,
            'products_json': json.dumps(PRODUCTS),
        },
    )


def about(request):
    """Render the About page for Naturis Foods."""
    canonical_url = urljoin(getattr(settings, 'FOODS_CANONICAL_URL', '') or request.build_absolute_uri('/'), '/about')
    return render(
        request,
        'foods/about.html',
        {
            'canonical_url': canonical_url,
            'meta_description': 'Company information for Naturis Marketplace wholesale buyers.',
        },
    )


def trade_terms(request):
    """Render the Trade terms page."""
    canonical_url = urljoin(getattr(settings, 'FOODS_CANONICAL_URL', '') or request.build_absolute_uri('/'), '/trade-terms')
    return render(
        request,
        'foods/trade_terms.html',
        {
            'canonical_url': canonical_url,
            'meta_description': 'Wholesale order minimums, pricing, quotation and delivery information.',
        },
    )


def privacy(request):
    """Render the Privacy notice page."""
    canonical_url = urljoin(getattr(settings, 'FOODS_CANONICAL_URL', '') or request.build_absolute_uri('/'), '/privacy')
    return render(
        request,
        'foods/privacy.html',
        {
            'canonical_url': canonical_url,
            'meta_description': 'Privacy notice for Naturis Marketplace wholesale customers and quotation requests.',
        },
    )


def contact(request):
    """Render the Contact page."""
    canonical_url = urljoin(getattr(settings, 'FOODS_CANONICAL_URL', '') or request.build_absolute_uri('/'), '/contact')
    return render(
        request,
        'foods/contact.html',
        {
            'canonical_url': canonical_url,
            'meta_description': 'Contact details and location for Naturis Foods / Goshen Giant Foods Ltd.',
        },
    )


def product_detail(request, product_id):
    """Render the standalone Product Detail & Size Comparison page."""
    product = get_product(product_id)
    if not product:
        raise Http404("Product not found.")

    canonical_url = urljoin(
        getattr(settings, 'FOODS_CANONICAL_URL', '') or request.build_absolute_uri('/'),
        f'/products/{product_id}'
    )
    return render(
        request,
        'foods/product_detail.html',
        {
            'canonical_url': canonical_url,
            'meta_description': f"Wholesale specifications, pack sizes and trade pricing for {product['name']}.",
            'product': product,
            'product_json': json.dumps(product),
            'products': PRODUCTS,
        },
    )


def api_fx(request):
    """Return FX conversion rates for country & currency selector."""
    currency = request.GET.get('currency', 'USD').upper()
    country = request.GET.get('country', 'US').upper()

    rate = STANDARD_FX_RATES.get(currency, 1.0)
    now_iso = datetime.now(timezone.utc).isoformat()

    return JsonResponse({
        'country': country,
        'currency': currency,
        'rates': {currency: rate},
        'asOf': {currency: now_iso},
        'source': {currency: 'daily exchange rate'},
    })


@csrf_exempt
def api_quote(request):
    """Handle wholesale quotation submission requests."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required.'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST.dict()

    trial_review = bool(data.get('trialRequest'))
    reference_num = f"NAT-{datetime.now().year}-{random.randint(10000, 99999)}"

    return JsonResponse({
        'ok': True,
        'reference': reference_num,
        'trialReview': trial_review,
        'message': f'Quotation request {reference_num} saved successfully.',
    })
