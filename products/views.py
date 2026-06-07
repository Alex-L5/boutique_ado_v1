from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q  # if the query isn't blank a special object from Jango.db.models called Q is used to generate a search query
from .models import Product, Category  

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None  # starting the query as none at the top of this view to ensure we don't get an error when loading the products page without a search term
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey  # set sort from none to that sort key
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))  # we need to first annotate all the products with a new field in order to allow case-insensitive sorting on the field, eg name field
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)  # we use the order by model method in order to actually sort the products        

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)  # double underscore syntax is common when making queries in django
            categories = Category.objects.filter(name__in=categories)  # looking for the name field of the category model as category and product are related with a foreign key          

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)  # the pipe here is what generates the or statement and the i in front of contains makes the queries case insensitive
            products = products.filter(queries)  # filter method in order to actually filter the products

    current_sorting = f'{sort}_{direction}'  # string formatting in order to return the current sorting methodology to the template
    
    context = {
        'products': products,
        'search_term': query,  # in the template
        'current_categories': categories,  # list of strings of category names passed through the URL converted into a list of actual category objects, so that we can access all their fields in the template 
        'current_sorting': current_sorting,
    }
    
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)