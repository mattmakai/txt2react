from datetime import datetime

from django.conf import settings
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
    def get_queryset(self):
        return ReactionEvent.objects.filter( \
            customer=self.request.user.get_profile())

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
            purchased_number = numbers[0].purchase()
        purchased_number.update(sms_application_sid=settings.TWILIO_APP_SID)

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
        # needs error handling
        to_number = request.POST.get('To')
        event = ReactionEvent.objects.get(phone_number=to_number)
        r.event = event
        r.phone_number = request.POST.get('From')
        r.message = request.POST.get('Body')
        r.save()
        resp = twilio.twiml.Response()
        resp.message("Thank you for your feedback on the %s event. If you " + \
                     "are seeking an answer to a specific question, please" + \
                     " make sure you included your Twitter handle for a " + \
                     "direct response." % (str(event.name),))
    else:
        resp = "This method requires a POST HTTP request."
    return HttpResponse(str(resp))

