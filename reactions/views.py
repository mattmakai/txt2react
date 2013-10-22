from django.views.generic import ListView

from braces.views import LoginRequiredMixin

from payments.models import Customer
from .models import ReactionEvent


class ReactionsListView(LoginRequiredMixin, ListView):
    model = ReactionEvent


