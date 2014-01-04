from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView

from braces.views import LoginRequiredMixin
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

def respond_to_msg(request):
    if request.method == 'POST':
        r = Reaction()
        # temp
        r.event = ReactionEvent.objects.get(pk=1)
        r.phone_number = request.POST.get('From')
        r.message = request.POST.get('Message')
        r.save()
    resp = twilio.twiml.Response()
    resp.message("Thank you for your feedback! If you have a specific " + \
        "question, please make sure you included your Twitter handle so I " + \
        "can get back to you directly.")
    return HttpResponse(str(resp))
