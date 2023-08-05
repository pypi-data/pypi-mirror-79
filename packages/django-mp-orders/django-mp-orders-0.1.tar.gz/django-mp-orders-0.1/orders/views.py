
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from cart.lib import get_cart

from orders.utils import send_new_order_notifications
from orders.forms import CheckoutForm


@transaction.atomic
def checkout(request):

    form = CheckoutForm(
        initial={'mobile': '+380'},
        data=request.POST or None)

    if request.method == 'POST' and form.is_valid():

        cart = get_cart(request)

        order = form.save(commit=False)

        order.delivery = form.fields['delivery'].get_delivery_method()
        order.address = form.fields['delivery'].get_address()

        order.save()

        for item in cart.items:
            order.items.create(
                product_id=item.id,
                qty=item.qty,
                **item.price_values)

        cart.clear()

        send_new_order_notifications(request, order)

        message = render_to_string(
            'orders/new_order_message.html', {'order': order})

        messages.success(request, mark_safe(message))

        return redirect('home')

    return render(request, 'orders/checkout.html', {'form': form})
