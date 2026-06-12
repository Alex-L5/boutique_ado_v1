from decimal import Decimal
from django.conf import settings

def bag_contents(request):  # context processor to make the dictionary available to all templates across the entire application

    bag_items = []  # empty list for the bag items to live in
    total = 0
    product_count = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:  # free delivery customer incentive
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)  # decimal function since this is a financial transaction and using float is susceptible to rounding errors
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total  # free delivery if the customer just buys a couple more items
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total  # delivery charge added to the total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }  # adding all these items to the context (dictionary) so they'll be available in apps and templates across the site      

    return context
