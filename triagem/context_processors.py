from django.conf import settings


def _organization_initials(name):
    parts = [part for part in (name or '').split() if part]
    if not parts:
        return 'C2'
    if len(parts) == 1:
        return parts[0][:2].upper()
    return ''.join(part[0] for part in parts[:2]).upper()


def app_branding(request):
    organization_name = settings.C2TA_ORGANIZATION_NAME
    return {
        'app_branding': {
            'product_name': settings.C2TA_PRODUCT_NAME,
            'product_tagline': settings.C2TA_PRODUCT_TAGLINE,
            'organization_name': organization_name,
            'organization_tagline': settings.C2TA_ORGANIZATION_TAGLINE,
            'organization_logo_url': settings.C2TA_ORGANIZATION_LOGO_URL,
            'organization_logo_alt': settings.C2TA_ORGANIZATION_LOGO_ALT,
            'organization_initials': _organization_initials(organization_name),
        }
    }