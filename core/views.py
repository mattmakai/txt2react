from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from payments.models import Customer



@login_required
def generate_customer_profile(req):
    """
        If a user logs in without a customer profile this will generate
        one and send them on their way.
    """
    try:
        req.user.get_profile()
    except Exception as e:
        c = Customer.objects.create(user=req.user)
        c.save()
    return HttpResponseRedirect(reverse('reactions_list'))


class ContactView(TemplateView):
    template_name = "core/contact.html"
    
    def get_context_data(self, **kwargs):
            context = super(ContactView, self).get_context_data(**kwargs)
            context['is_contact'] = True
            return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class LearnMoreView(TemplateView):
    def get_context_data(self, **kwargs):
            context = super(LearnMoreView, self).get_context_data(**kwargs)
            context['is_learn_more'] = True
            return context

    template_name = "core/learn_more.html"


class LandingView(TemplateView):
    template_name = "core/landing.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("reactions_list"))
        else:
            return super(LandingView, self).get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
            context = super(LandingView, self).get_context_data(**kwargs)
            context['is_landing'] = True
            return context


class SignUpView(TemplateView):
    template_name = "core/sign_up.html"


class LoginView(TemplateView):
    template_name = "core/login.html"

    def get_success_url(self):
        return reverse('reactions_list')
        

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("reactions_list"))
        else:
            return super(LoginView, self).get(self.request, *args, **kwargs)


def signout(req):
    logout(req)
    return HttpResponseRedirect(reverse("landing"))

