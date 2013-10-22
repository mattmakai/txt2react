from django.core.urlresolvers import reverse
from django.test import TestCase

from .helpers import create_customer
from payments.models import Customer


class SmokeTestPages(TestCase):
    """
        Smoke tests pages to ensure no sudden 500 errors go unnoticed.
    """
    def test_landing_page(self):
        resp = self.client.get(reverse('landing'))
        self.assertTrue(resp.status_code, 200)
    
    def test_login_page(self):
        resp = self.client.get(reverse('signin'))
        self.assertTrue(resp.status_code, 200)
    
    def test_about_page(self):
        resp = self.client.get(reverse('about'))
        self.assertTrue(resp.status_code, 200)
    
    def test_contact_page(self):
        resp = self.client.get(reverse('contact'))
        self.assertTrue(resp.status_code, 200)


class UtilsTest(TestCase):
    """
        Tests the helpers.py file functions in core app.
    """
    def test_create_customer(self):
        self.assertEqual(Customer.objects.all().count(), 0)
        c = create_customer("john.smith@gmail.com", "x", "John", "Smith")
        self.assertEqual(Customer.objects.all().count(), 1)

