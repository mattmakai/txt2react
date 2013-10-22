from django.conf import settings

from .helpers import generate_intercom_user_hash

def analytics(request):
    if hasattr(request.user, 'email'):
        intercom_user_hash = \
            str(generate_intercom_user_hash(request.user.email))
    else:
        intercom_user_hash = '' # blank for development mode

    return {'INTERCOM_IO_APP_ID': settings.INTERCOM_IO_APP_ID,
            'INTERCOM_IO_API_SECRET': settings.INTERCOM_IO_API_SECRET,
            'INTERCOM_IO_USER_HASH': intercom_user_hash}


def production_mode(request):
    return {'PRODUCTION_MODE': settings.PRODUCTION_MODE,}
