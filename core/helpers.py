import hmac, hashlib

from django.conf import settings
from django.contrib.auth.models import User

from payments.models import Customer

"""
    helpers.py contains all util functions not used by models.py to avoid
    circular imports 
"""

def create_customer(email, passwd, first, last, staff=False, superuser=False):
    u = User.objects.create_user(username=email, email=email,
        password=passwd)
    u.first_name = first
    u.last_name = last
    u.is_staff = staff
    u.is_superuser = superuser
    u.is_active = True
    u.save()
    c = Customer()
    c.user = u
    c.save()
    return c


def generate_intercom_user_hash(user_id_or_email):
    return hmac.new(settings.INTERCOM_IO_API_SECRET, user_id_or_email, 
        digestmod=hashlib.sha256).hexdigest()


