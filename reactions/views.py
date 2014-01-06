from datetime import datetime

from django.conf import TWILIO_APP_SID
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView

from braces.views import LoginRequiredMixin
from twilio.rest import TwilioRestClient
import twilio.twiml

from payments.models import Customer
from .forms import ReactionEventForm
from .models import ReactionEvent, Reaction


class EventsListView(LoginRequiredMixin, ListView):
    model = ReactionEvent

    def get(self, *args, **kwargs):
        try:
            self.request.user.get_profile()
        except Exception as e:
            c = Customer.objects.create(user=self.request.user)
            c.save()
        return super(EventsListView, self).get(self.request, *args, **kwargs)


class CreateEventView(LoginRequiredMixin, CreateView):
    model = ReactionEvent
    form_class = ReactionEventForm

    def form_valid(self, form):
        event = ReactionEvent()
        
        # this should be async, and customizable
        client = TwilioRestClient()
        numbers = client.phone_numbers.search(area_code=202)
        event.phone_number = numbers[0].phone_number
        if numbers:
            numbers[0].purchase()
        numbers[0].update(sms_application_sid=TWILIO_APP_ID)

        event.customer = self.request.user.get_profile()
        event.name = form.cleaned_data['name']
        event.url = form.cleaned_data['url']
        event.location = form.cleaned_data['location']
        # temp
        event.event_date = datetime.now()
        event.save()
        return HttpResponseRedirect(reverse('reactions_list'))


class EventDetailView(LoginRequiredMixin, DetailView):
    model = ReactionEvent


@csrf_exempt
def respond_to_msg(request):
    if request.method == 'POST':
        r = Reaction()
        # temp
        r.event = ReactionEvent.objects.all()[0]
        r.phone_number = request.POST.get('From')
        r.message = request.POST.get('Body')
        r.save()
    resp = twilio.twiml.Response()
    resp.message("Thank you for your feedback! If you have a specific " + \
        "question, please make sure you included your Twitter handle so I " + \
        "can get back to you directly.")
    return HttpResponse(str(resp))
