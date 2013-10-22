from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

import stripe

import .paypal
from .models import Customer, Purchase


TEMPLATE_PATH = 'payments/'

def purchased(req, uid, id):
  proof = get_object_or_404(PurchaseItem, pk=id)
  c = get_object_or_404(Customer, pk=uid)
  if req.REQUEST.has_key('tx'):
    tx = req.REQUEST['tx']
    try:
      is_existing = Purchase.objects.get(tx=tx)
      return HttpResponse('Duplicate transaction.')
    except Purchase.DoesNotExist:
      result = paypal.Verify(tx)
      try:
        result.amount()
      except KeyError as ke:
        return HttpResponse('invalid transaction')
      if result.success() and proof.price == result.amount(): # valid
        return successfulPayment()
      else: # didn't validate
        return HttpResponse('purchase validation error')
  else:
    return HttpResponse('error, no tx found')


@login_required
@csrf_protect
def stripePayment(req):
  if req.method == 'POST':
    customer = req.user.get_profile()
    token = req.POST.get('stripeToken', '')
    proof_name = req.POST.get('item_name', '')
    if token == '' or proof_name == '':
      # error
      return HttpResponse('error')
    else:
      stripe.api_key = settings.STRIPE_SECRET
      proof = get_object_or_404(Proof, title=proof_name)

      charge = stripe.Charge.create(
        amount = proof.price,
        currency="usd",
        card=token,
        description=str(customer.user.email)
      )
      return successfulPayment(req, customer, proof)
  elif req.method == 'GET':
    return HttpResponse("This URL requires a POST request.")


def successfulPayment(req, c, proof, tx=None):
    purchase = Purchase(customer=c, purchase_date=datetime.now(),
        paid_for=True, tx=tx, amount=proof.price)
    purchase.save()
    purchase.proofs.add(proof)
    purchase.save()
    p = {}
    messages.add_message(req, messages.INFO, \
        "Thank you for your purchase.")
    return HttpResponseRedirect('/home/proof/' + proof.url + '/')


@login_required
def receipt(req, pid):
    customer = req.user.get_profile()
    params = {'purchase': get_object_or_404(Purchase, pk=pid, 
        customer=customer),}
    params['price_paid'] = params['purchase'].amount / 100.
    return render(TEMPLATE_PATH + 'receipt.html', params)

