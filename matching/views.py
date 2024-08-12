from django.shortcuts import render, redirect
from django.db import transaction
from .models import PendingOrder, CompletedOrder
from .forms import OrderForm

def order_and_match_page(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            buyer_qty = form.cleaned_data['buyer_qty']
            buyer_price = form.cleaned_data['buyer_price']
            seller_price = form.cleaned_data['seller_price']
            seller_qty = form.cleaned_data['seller_qty']

            # Start a transaction to ensure data integrity
            with transaction.atomic():
                # Add new order to PendingOrder table
                new_order = PendingOrder(
                    buyer_qty=buyer_qty,
                    buyer_price=buyer_price,
                    seller_price=seller_price,
                    seller_qty=seller_qty
                )
                new_order.save()

                # Match orders
                # match_orders()

            return redirect('order_and_match_page')
    else:
        form = OrderForm()

    # Get pending and completed orders for display
    pending_orders = PendingOrder.objects.all()
    completed_orders = CompletedOrder.objects.all()

    return render(request, 'order_and_match_page.html', {
        'form': form,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders
    })

def match_orders():
    pending_orders = PendingOrder.objects.all().order_by('buyer_price')
    for pending in pending_orders:
        if not pending.seller_qty or not pending.buyer_qty:
            continue

        # Match orders where buyer price >= seller price
        matching_sellers = PendingOrder.objects.filter(
            seller_price__lte=pending.buyer_price,
            seller_qty__gt=0
        ).order_by('seller_price')

        for seller in matching_sellers:
            if pending.buyer_qty <= 0:
                break

            qty_to_match = min(pending.buyer_qty, seller.seller_qty)
            price_to_match = seller.seller_price

            # Update CompletedOrder table
            completed_order, created = CompletedOrder.objects.get_or_create(
                price=price_to_match,
                defaults={'qty': 0}
            )
            if not created:
                completed_order.qty += qty_to_match
                completed_order.save()

            # Update PendingOrder table
            pending.buyer_qty -= qty_to_match
            seller.seller_qty -= qty_to_match

            if pending.buyer_qty <= 0:
                pending.delete()
                break
            else:
                pending.save()

            if seller.seller_qty <= 0:
                seller.delete()

