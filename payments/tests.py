from django.test import TestCase
from .models import Purchase, PurchaseItem


class TestStripePayment(TestCase):
    def setUp(self):
        pass        
