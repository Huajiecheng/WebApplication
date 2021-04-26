from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from project.forms import CreateEntry, CreateRestaurant, CreateReview, CreateReviewImage, ProfileAddressForm
from project.models import Entry, Restaurant, Order, Cart, CartEntry, Review, ReviewImage, OrderEntry, AddressProfile

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.db.models import Q
from project.forms import LoginForm, RegisterForm
from project.forms import ProfileAddressForm, AddressForm
import json

state_abbr = {'Alabama':'AL','Alaska':'AK','Arizona': 'AZ','Arkansas':'AR','California':'CA','Colorado':'CO',
              'Connecticut':'CT','District of Columbia':'DC','Delaware':'DE','Florida':'FL','Georgia':'GA',
              'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY',
              'Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN',
              'Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH',
              'New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND',
              'Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC',
              'South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA',
              'Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}

states_choices = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", 
                  "Colorado", "Connecticut", "Delaware", "District Of Columbia", 
                  "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", 
                  "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
                  "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
                  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
                  "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
                  "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
                  "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                  "West Virginia", "Wisconsin", "Wyoming"]

# Create your views here.
def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'project/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'project/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    if form.cleaned_data['username'] == "SEadmin":
        return redirect(reverse('admin'))
    else:
        return redirect(reverse('home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'project/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'project/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    login(request, new_user)
    if form.cleaned_data['username'] == "SEadmin":
        new_restaurant = Restaurant(admin_user = new_user)
        new_restaurant.save()
        return redirect(reverse('admin'))
    else:
        new_profile = AddressProfile(user = new_user)
        new_profile.save()
        new_cart = Cart(owner = new_user)
        new_cart.save()
        return redirect(reverse('home'))

@login_required
def get_res_image(request):
    restaurant = get_object_or_404(Restaurant, id=1)
    if not restaurant.photo:
        raise Http404

    return HttpResponse(restaurant.photo)


@login_required
def get_image(request, id):
    item = get_object_or_404(ReviewImage, id=id)
    if not item.image:
        raise Http404

    return HttpResponse(item.image)

@login_required
def get_photo(request, id):
    profile = get_object_or_404(AddressProfile,id=id)
    if not profile.picture:
        raise Http404

    return HttpResponse(profile.picture)


# admin page for restaurant owner
@login_required
def admin_page(request, option="menu"): 
    context = {}
    # only owner can modify the restaurant info
    if request.user.username != "SEadmin":
        print("ERROR in admin_page")
        context['error'] = "You do not have access to this page."
        return render(request,'project/error.html',context)
    new_order_amount = Order.objects.filter(status="INPROGRESS").count()
    # get previous info, and loaded it when the method is GET
    restaurant = get_object_or_404(Restaurant, admin_user=request.user)
    init = {'name': restaurant.name,
    'location':restaurant.location,
    'average_rating': restaurant.average_rating,
    'description':restaurant.description,
    'photo':restaurant.photo,
    'content_type':restaurant.content_type,
    'deliveryTime':restaurant.deliveryTime,}
    if request.method == 'GET':
        context = {'option':option,
        'form': CreateEntry(),
        'restaurant': restaurant,
        'restaurantForm':CreateRestaurant(initial=init)}
        if option=="menu":
            context['entries']=Entry.objects.all()
            context['entry_types'] = ["Appetizer","Soup","Salad","Entree","Beverage","Dessert"]
        else:
            context['reviews'] = Review.objects.all().order_by('-review_time')
        context['new_order_amount'] = new_order_amount
        return render(request,'project/admin_page.html', context)

    # POST
    create_restaurant = CreateRestaurant(request.POST, request.FILES)
    if not create_restaurant.is_valid():
        context = {'option': option,
        'error': "Failed to update restaurant info.",
        'form': CreateEntry(),
        'restaurant': restaurant,
        'restaurantForm':CreateRestaurant(initial=init)}
        if option=="menu":
            context['entries']=Entry.objects.all()
            context['entry_types'] = ["Appetizer","Soup","Salad","Entree","Beverage","Dessert"]
        else:
            context['reviews'] = Review.objects.all().order_by('-review_time')
        context['new_order_amount'] = new_order_amount
        return render(request,'project/admin_page.html', context)

    # update any info that user entered
    restaurant.name = create_restaurant.cleaned_data['name']
    # in this case, we allow user to update info without uploading a new picture
    if create_restaurant.cleaned_data['photo']:
        restaurant.photo = create_restaurant.cleaned_data['photo']
        restaurant.content_type = create_restaurant.cleaned_data['photo'].content_type
    restaurant.location = create_restaurant.cleaned_data['location'] 
    restaurant.description = create_restaurant.cleaned_data['description']
    restaurant.deliveryTime = create_restaurant.cleaned_data['deliveryTime']
    restaurant.save()

    init = {'name': restaurant.name,
    'location':restaurant.location,
    'average_rating': restaurant.average_rating,
    'description':restaurant.description,
    'photo':restaurant.photo,
    'content_type':restaurant.content_type,
    'deliveryTime':restaurant.deliveryTime,}
    context = {'option': option,
        'message': "Profile updated",
        'form': CreateEntry(),
        'restaurant': restaurant,
        'restaurantForm':CreateRestaurant(initial=init),
    }
    if option=="menu":
        context['entries']=Entry.objects.all()
        context['entry_types'] = ["Appetizer","Soup","Salad","Entree","Beverage","Dessert"]
    else:
        context['reviews'] = Review.objects.all().order_by('-review_time')
    context['new_order_amount'] = new_order_amount
    return render(request, 'project/admin_page.html', context)
    

@login_required
def add_entry(request):
    restaurant = get_object_or_404(Restaurant, admin_user=request.user)
    init = {'name': restaurant.name,
        'location':restaurant.location,
        'average_rating': restaurant.average_rating,
        'description':restaurant.description,
        'photo':restaurant.photo,
        'content_type':restaurant.content_type,
        'deliveryTime':restaurant.deliveryTime,
    }
    context = {'option': "menu",
        'restaurant': restaurant,
        'restaurantForm':CreateRestaurant(initial=init),
        'entry_types':["Appetizer","Soup","Salad","Entree","Beverage","Dessert"],
    }

    new_entry = Entry()
    form = CreateEntry(request.POST)
    if not form.is_valid():
        context['form'] = form
        context['error'] = "Failed to create entry"
    else:
        new_entry.name=form.cleaned_data['name']
        new_entry.price = form.cleaned_data['price']
        new_entry.description=form.cleaned_data['description']
        new_entry.entry_type=form.cleaned_data['entry_type']
        new_entry.save()
        context['message'] = 'Entry (' + new_entry.name + ') saved.'
        context['form'] = CreateEntry()

    context['entries'] = Entry.objects.all()
    return render(request, 'project/admin_page.html', context)

def convert_location_to_coordinate(location):
    latitude, longitude = float(location.split(',')[0][1:].strip()), float(location.split(',')[1][:-1].strip())

    return latitude, longitude
@login_required
def map_location(request):
    context = {}
    

    print(context)
    return render(request, 'project/location_map.html', context)

@login_required
def profile(request):
    context = {}
    cart = get_object_or_404(Cart, owner=request.user)
    entries_in_cart = CartEntry.objects.filter(cart=cart)
    context['cartItems'] = entries_in_cart
    context['count'] = CartEntry.objects.filter(cart=cart).count()
    profile = get_object_or_404(AddressProfile, user = request.user)
    init = {'postal_code': profile.postal_code,
        'state':profile.state,
        'street_1': profile.street_1,
        'street_2':profile.street_2,
    }
    context['form'] = ProfileAddressForm(initial=init)
    if request.method == 'GET':
        context['profile'] = profile
        return render(request, 'project/profile.html', context)
    form = ProfileAddressForm(request.POST, request.FILES)
    if not form.is_valid():
        context['error'] = "Failed to update profile"
        context['profile'] = profile
        context['form'] = form
        return render(request, 'project/profile.html', context)
    else:
        if form.cleaned_data['picture']:
            profile.picture = form.cleaned_data['picture']
            profile.content_type = form.cleaned_data['picture'].content_type
        profile.postal_code = form.cleaned_data['postal_code']
        profile.state = form.cleaned_data['state']
        profile.street_1 = form.cleaned_data['street_1']
        profile.street_2 = form.cleaned_data['street_2']
        profile.save()
        init = {'postal_code': profile.postal_code,
        'state':profile.state,
        'street_1': profile.street_1,
        'street_2':profile.street_2,
        }
        context['form'] = ProfileAddressForm(initial=init)
        context['profile'] = profile
    return render(request, 'project/profile.html', context)

@login_required
def edit_entry(request,id):
    entry = get_object_or_404(Entry, id=id)
    restaurant = get_object_or_404(Restaurant, admin_user=request.user)
    init = {'name': restaurant.name,
        'location':restaurant.location,
        'average_rating': restaurant.average_rating,
        'description':restaurant.description,
        'photo':restaurant.photo,
        'content_type':restaurant.content_type,
        'deliveryTime':restaurant.deliveryTime,
    }
    context = {'option': "menu",
        'restaurant': restaurant,
        'restaurantForm':CreateRestaurant(initial=init),
        'entries': Entry.objects.all(),
        'entry_types':["Appetizer","Soup","Salad","Entree","Beverage","Dessert"],
    }

    init={
        'name': entry.name,
        'price': entry.price,
        'description': entry.description,
        'entry_type':entry.entry_type,
    }
    context['editEntry'] = entry
    context['editForm'] = CreateEntry(initial=init)
    context['form'] = CreateEntry()
    if request.method == 'GET':
        return render(request, 'project/admin_page.html', context)

    form = CreateEntry(request.POST)
    if not form.is_valid():
        context['error'] = "Failed to update entry"
        return render(request, 'project/admin_page.html', context)


    entry.name = form.cleaned_data['name']
    entry.price = form.cleaned_data['price']
    entry.description = form.cleaned_data['description']
    entry.entry_type = form.cleaned_data['entry_type']
    entry.save()

    context['entries'] = Entry.objects.all()
    context['message'] = "Entry successfully updated!"
    del context['editEntry']
    return render(request, 'project/admin_page.html', context)


@login_required
def delete_entry(request,id):
    entry = get_object_or_404(Entry, id=id)
    print("DELETE")

    restaurant = get_object_or_404(Restaurant, admin_user=request.user)
    init = {'name': restaurant.name,
        'location':restaurant.location,
        'average_rating': restaurant.average_rating,
        'description':restaurant.description,
        'photo':restaurant.photo,
        'content_type':restaurant.content_type,
        'deliveryTime':restaurant.deliveryTime,
    }
    context = {'option': "menu",
        'restaurant': restaurant,
        'restaurantForm':CreateRestaurant(initial=init),
        'entries': Entry.objects.all(),
        'entry_types':["Appetizer","Soup","Salad","Entree","Beverage","Dessert"],
    }

    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
    else:
        entry.delete()
        context['message'] = 'Entry deleted.'

    context['entries'] = Entry.objects.all()
    context['form'] = CreateEntry()
    return render(request, 'project/admin_page.html', context)



@login_required
def main_page(request, option="menu"):
    if request.user.username== "SEadmin":
        return redirect(reverse('admin'))
    context = {'option':option}
    entries = Entry.objects.all()
    # TODO here I find the restaurant by hard-coding its id to 1
    restaurant = get_object_or_404(Restaurant,id=1)
    cart = get_object_or_404(Cart,owner=request.user)
    
    context['restaurant'] = restaurant
    context['cartItems'] = CartEntry.objects.filter(cart=cart).iterator()
    context['count'] = CartEntry.objects.filter(cart=cart).count()
    if option== "menu":
        context['entries'] = entries
        context['entry_types'] = ["Appetizer","Soup","Salad","Entree","Beverage","Dessert"]
    else:
        context['reviews'] = Review.objects.all().order_by('-review_time')
        context['user'] = request.user
    if request.method == 'GET':
        return render(request,'project/main_page.html', context)
        
    return render(request, 'project/main_page.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'GET':
        context= {'error': "You cannot access this page using GET request."}
        return render(request,'project/admin_page.html',context)
    cart = get_object_or_404(Cart, owner=request.user)
    id = int(request.POST.get("add_entry_id", None))
    count = int(request.POST.get("add_entry_count", None))
    context = {'option':"menu"}
    entries = Entry.objects.all()
    # TODO here I find the restaurant by hard-coding its id to 1
    restaurant = get_object_or_404(Restaurant,id=1)
    context['entries'] = entries
    context['restaurant'] = restaurant
    context['entry_types'] = ["Appetizer","Soup","Salad","Entree","Beverage","Dessert"]

    add_entry = get_object_or_404(Entry, id=id)

    if CartEntry.objects.filter(cart=cart, entry=add_entry).exists():
        added_cartEntry = get_object_or_404(CartEntry,cart=cart, entry=add_entry)
        added_cartEntry.quantity=added_cartEntry.quantity+count
        added_cartEntry.save()
    else:
        new_cartEntry = CartEntry(cart=cart, entry=add_entry,quantity=count)
        new_cartEntry.save()

    context['cartItems'] = CartEntry.objects.filter(cart=cart).iterator()
    context['count'] = CartEntry.objects.filter(cart=cart).count()
    return render(request, 'project/main_page.html', context)

@login_required
def delete_cart_item(request, id):
    context = {}
    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, "project/error.html", context)
    cartEntry = get_object_or_404(CartEntry, id=id)
    cartEntry.delete()
    context['message'] = 'Item deleted.'

    return redirect(reverse('payment'))

def delete_all_items(request):
    context = {}
    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, "project/error.html", context)
    cart = get_object_or_404(Cart, owner=request.user)
    cartEntries = CartEntry.objects.filter(cart=cart)
    for cartEntry in cartEntries.iterator():
        cartEntry.delete()
    context['message'] = 'All items deleted.'

    return redirect(reverse('payment'))


@login_required
def edit_cart_item(request, id):
    context = {}
    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, "project/error.html", context)
    quantity = int(request.POST.get("quantity", None))
    cartEntry = get_object_or_404(CartEntry, id=id)
    cartEntry.quantity = quantity
    cartEntry.save()
    context['message'] = 'Item updated.'

    return redirect(reverse('payment'))



@login_required
def payment(request):
    context = {}
    cart = get_object_or_404(Cart, owner=request.user)
    entries_in_cart = CartEntry.objects.filter(cart=cart)
    restaurant = get_object_or_404(Restaurant,id=1)
    total = 0
    for i in entries_in_cart:
        total += i.entry.price*i.quantity
    context["total"] = total
    context['cartItems'] = entries_in_cart
    context['count'] = CartEntry.objects.filter(cart=cart).count()
    #Order.objects.filter(Q(customer = request.user)&Q(status = "CANCELLED")).delete()
    order = Order.objects.filter(Q(customer = request.user)&Q(status = "CANCELLED"))

    if order.count()==0:
        new_order = Order(status = "CANCELLED", customer = request.user,order_time = datetime.now(), amount = total)
        profile = get_object_or_404(AddressProfile, user = request.user)       
        if profile.postal_code !='' and profile.street_1 != '' and profile.street_2 != '':
            state= state_abbr[states_choices[int(profile.state)-1]]
            new_order.location = "%s %s, %s %s, USA" %(profile.street_2,profile.street_1,state,profile.postal_code)
        new_order.save()
        for i in entries_in_cart:
            new_items = OrderEntry(entry = i.entry,order = new_order,quantity=i.quantity)
            new_items.save()     
    else:
        new_order = order[0]
        if new_order.location=='':
            profile = get_object_or_404(AddressProfile, user = request.user)
            if profile.postal_code !='' and profile.street_1 != '' and profile.street_2 != '': 
                state= state_abbr[states_choices[int(profile.state)-1]]             
                new_order.location = "%s %s, %s %s, USA" %(profile.street_2,profile.street_1,state,profile.postal_code)
        for i in entries_in_cart:
            if OrderEntry.objects.filter(Q(order=new_order)&Q(entry=i.entry)).exists():
                item = get_object_or_404(OrderEntry,order=new_order, entry=i.entry)
                item.quantity = i.quantity
                item.save()
            else:
                item = OrderEntry(entry = i.entry,order = new_order,quantity=i.quantity)
                item.save()
        new_order.amount = total
        new_order.order_time = datetime.now()
        new_order.save()
    context["order"] = new_order
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_REVEIVER_EMAIL,
        "amount": total,
        "item_name": "Food from {}".format(restaurant.name),
        "invoice": "invoice555-{}".format(new_order.id),
        "currency_code": 'USD',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context["form"] = form
    context["AddrForm"] = AddressForm()
    return render(request, "project/payment.html", context)

@login_required   
def add_address(request):
    if request.method == 'GET':
        context= {'error': "You cannot access this page using GET request."}
        return render(request, "project/error.html", context)
    order_id = int(request.POST.get("orderId", None))
    order = get_object_or_404(Order, id=order_id)
    form = AddressForm(request.POST)
    if not form.is_valid():
        return redirect(reverse('payment'))

    postal_code = form.cleaned_data['postal_code']
    state = form.cleaned_data['state']
    street_1 = form.cleaned_data['street_1']
    street_2 = form.cleaned_data['street_2']
    state_name = state_abbr[states_choices[int(state)-1]]
    location = "%s %s, %s %s, USA" %(street_2,street_1,state_name,postal_code)
    order.location = location 
    order.save()
    return redirect(reverse('payment'))

@login_required   
def add_review(request):
    if request.method == 'GET':
        context= {'error': "You cannot access this page using GET request."}
        return render(request, "project/error.html", context)
    restaurant = get_object_or_404(Restaurant,id=1)
    order_id = int(request.POST.get("orderId", None))
    order = get_object_or_404(Order, id=order_id)
    profile = get_object_or_404(AddressProfile, user=request.user)
    review = Review(order = order, profile=profile)
    create_review = CreateReview(request.POST)
    
    if not create_review.is_valid():
        print('not valid')
        return redirect(reverse('order', args=[order_id]))
    review.rating = create_review.cleaned_data['rating']
    review.review_text = create_review.cleaned_data['review_text']
    review.review_time = datetime.now()
    review.save()
    restaurant.average_rating = (restaurant.average_rating * restaurant.num_review + float(review.rating))/(restaurant.num_review + 1)
    restaurant.num_review = restaurant.num_review + 1
    restaurant.save()
    create_reviewImage = CreateReviewImage(request.POST,request.FILES)
    files = request.FILES.getlist('image')
    print(len(files))
    if not create_reviewImage.is_valid():
        print('not valid')
        return redirect(reverse('order', args=[order_id]))
    for f in files:
        file_instance = ReviewImage(image=f)
        file_instance.save()
        review.images.add(file_instance)
    return redirect(reverse('order', args=[order_id]))
    
@login_required
def delete_review(request,id):
    context = {}
    if request.method != 'POST':
        context['error'] = 'Deletes must be done using the POST method'
        return render(request, "project/error.html", context)
    review = get_object_or_404(Review, id=id)
    restaurant = get_object_or_404(Restaurant,id=1)
    if restaurant.num_review > 1:
        restaurant.average_rating = (restaurant.average_rating * restaurant.num_review - float(review.rating))/(restaurant.num_review - 1)
    else:
        restaurant.average_rating = 0
    restaurant.num_review = restaurant.num_review - 1
    restaurant.save()
    review.delete()
    context['message'] = 'Entry deleted.'

    return redirect(reverse('home', args=["review"]))




@login_required
@csrf_exempt    
def payment_done(request):
    context = {}
    order = Order.objects.filter(customer = request.user).order_by('-order_time')[0]
    context["order_id"]=order.id
    return render(request, "project/payment_done.html",context)

@login_required
@csrf_exempt
def payment_cancelled(request):
    context = {}
    cart = get_object_or_404(Cart, owner=request.user)
    entries_in_cart = CartEntry.objects.filter(cart=cart)
    context['cartItems'] = entries_in_cart
    context['count'] = CartEntry.objects.filter(cart=cart).count()
    return render(request, "project/payment_cancelled.html",context)

@login_required
def orders(request):
    context = {}
    restaurant = get_object_or_404(Restaurant,id=1)
    context['restaurant_name'] = restaurant.name
    cart = get_object_or_404(Cart, owner=request.user)
    entries_in_cart = CartEntry.objects.filter(cart=cart)
    context['cartItems'] = entries_in_cart
    context['count'] = CartEntry.objects.filter(cart=cart).count()
    orders = Order.objects.filter(Q(customer = request.user)&(~Q(status="CANCELLED"))).order_by('-order_time')
    context["orders"]=orders
    return render(request, "project/orders.html",context)


@login_required
def order(request,id):
    cart = get_object_or_404(Cart, owner=request.user)
    entries_in_cart = CartEntry.objects.filter(cart=cart)
    order = get_object_or_404(Order,id=id)
    items = OrderEntry.objects.filter(order=order)
    context = {"items":items,"order":order}
    context['cartItems'] = entries_in_cart
    context['count'] = CartEntry.objects.filter(cart=cart).count()
    context['reviewForm'] = CreateReview()
    review = Review.objects.filter(order = order)
    if not Review.objects.filter(order = order).exists():
        context['writeReview'] = "writeReview"
    return render(request, "project/order.html",context)

@login_required
def admin_order(request,id):
    order = get_object_or_404(Order,id=id)
    if request.method == "POST":
        order.status = "COMPLETE"
        order.save()
    items = OrderEntry.objects.filter(order=order)
    context = {"items":items,"order":order}
    return render(request, "project/admin_order.html",context)

@login_required
@ensure_csrf_cookie
def orders_stream(request):
    return render(request, 'project/admin_orders.html')

@login_required
@ensure_csrf_cookie
def refresh_orders(request):
    orders_data = []
    orders = Order.objects.exclude(status="CANCELLED").order_by('order_time').order_by('status')
    for model_item in orders: 
        my_item = {
            'id': model_item.id,
            'location': model_item.location,
            'user': model_item.customer.id,
            'first_name': model_item.customer.first_name,
            'last_name': model_item.customer.last_name,
            'status': model_item.status,
            'time': model_item.order_time.isoformat(),
            'amount': str(model_item.amount),
        }
        orders_data.append(my_item)

    data = {'orders':orders_data}
    response_json = json.dumps(data)

    return HttpResponse(response_json, content_type='application/json')

@login_required
@ensure_csrf_cookie    
def refresh_done(request):
    order_data = []
    order = Order.objects.filter(customer = request.user).order_by('-order_time')[0]
    my_item = {
            'id': order.id,
            'status': order.status,
    }
    order_data.append(my_item)

    data = {'order':order_data}
    response_json = json.dumps(data)
    return HttpResponse(response_json, content_type='application/json')

@login_required
def directions(request,id):
    context = {}
    order = get_object_or_404(Order,id=id)
    context['order'] = order
    return render(request, "project/directions.html", context)