from django.db import models
from django.contrib.auth.models import User

from core.utils import create_slug
from core.models import BaseModel

class Customer(models.Model):
    user = models.ForeignKey(User)
    preferred_name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=255, unique=True)
    is_avatar_set = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    first_time_login = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = create_slug(Customer, unicode(self))
        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Purchase(BaseModel):
    customer = models.ForeignKey(Customer)
    purchase_date = models.DateTimeField()
    paid_for = models.BooleanField()
    tx = models.CharField(max_length=250, null=True, blank=True)
    amount = models.IntegerField()
    def __unicode__(self):
        return ' '.join(("Purchase on", str(self.purchase_date)))


class PurchaseItem(BaseModel):
    pass
