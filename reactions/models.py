from django.db import models

from core.utils import create_slug
from core.models import BaseModel
from payments.models import Customer

class ReactionEvent(BaseModel):
    customer = models.ForeignKey(Customer) 
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=2048, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    slug = models.CharField(max_length=255, unique=True)
    phone_number = models.IntegerField(blank=True, default=0)
    event_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = create_slug(ReactionEvent, unicode(self))
        super(ReactionEvent, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "%s on %s" % (self.name, str(self.event_date))


class Reaction(BaseModel):
    event = models.ForeignKey(ReactionEvent)
    slug = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=128)
    message = models.CharField(max_length=1024)
    received_timestamp = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = create_slug(Reaction, unicode(self))
        super(Reaction, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.message
