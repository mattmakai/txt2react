from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView

from braces.views import LoginRequiredMixin

from payments.models import Customer
from .forms import ReactionEventForm
from .models import ReactionEvent


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
