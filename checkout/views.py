import math
from django.http import JsonResponse, HttpResponse
from django_store import settings
from .forms import UserInfoForm, MyPayPalPaymentsForm
from .models import Transaction, PaymentMethod
from store.models import Product, Cart
from django.utils.translation import gettext as _
import stripe
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse


def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Stripe)
    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information.')
        }, status=400)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction': transaction.id
        }
    )
    return JsonResponse({
        'client_secret': intent['client_secret']
    })


def paypal_transaction(request):
    transaction = make_transaction(request, PaymentMethod.Paypal)
    if not transaction:
        return JsonResponse({
            'message': _('Please enter valid information.')
        }, status=400)

    form = MyPayPalPaymentsForm(initial={
        'business': settings.PAYPAL_EMAIL,
        'amount': transaction.amount,
        'invoice': transaction.id,
        'currency_code': settings.CURRENCY,
        'return_url': f'http://{request.get_host()}{reverse("store.checkout_complete")}',
        'cancel_url': f'http://{request.get_host()}{reverse("store.checkout")}',
        'notify_url': f'http://{request.get_host()}{reverse("checkout.paypal-webhook")}',
    })

    return HttpResponse(form.render())


def make_transaction(request, pm):
    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.items)

        total = 0
        for item in products:
            total += item.price

        if total <= 0:
            return None

        return Transaction.objects.create(
            customer=form.cleaned_data,
            session=request.session.session_key,
            payment_method=pm,
            items=cart.items,
            amount=math.ceil(total)
        )
