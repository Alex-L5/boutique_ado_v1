from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q  # if the query isn't blank a special object from Jango.db.models
from .models import Product  # called Q is used to generate a search query

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None  # starting the query as none at the top of this view to ensure we don't get an error when loading the products page without a search term

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)  # the pipe here is what generates the or statement and the i in front of contains makes the queries case insensitive
            products = products.filter(queries)  # filter method in order to actually filter the products

    context = {
        'products': products,
        'search_term': query,  # in the template  
    }
    
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)