from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):  # submitting the form to this view including the product id and the quantity
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))  # getting the quantity from the form and converting it to an integer since it'll come from the template as a string    
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})  # a HTTP session is used to allow information to be stored by the user. the variable bag (dictionary) accesses the requests session
# once in the view we'll get the bag variable if it exists in the session or create it if it doesn't
    if item_id in list(bag.keys()):  # if the item is already in the bag (a key in the bag dictionary matching this product id) then its quantity is incremented accordingly
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity  # a key of the items id within the bag dictionary (adding the item to the bag)  

    request.session['bag'] = bag  # putting the bag variable into the session or updating it    
    print(request.session['bag'])  # printing the shopping bag from the session in the add to bag view  
    return redirect(redirect_url)  # redirecting the user back to the redirect URL