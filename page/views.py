from datetime import datetime
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.core.paginator import Paginator
import razorpay
from django.conf import settings
from ecommerce.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET



client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))



def create_order(request):
    cart_items = AddItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    amount = int(total_price * 100)

    payment_order = client.order.create({'amount': amount, 'currency': "INR", 'payment_capture': '1'})
    payment_order_id = payment_order['id']

    context = {'amount': amount, 'api_key': RAZORPAY_API_KEY, 'order_id': payment_order_id, 'total_price': total_price}
    return render(request, 'payment.html', context)



def order_history(request):
    user_orders = OrderDetail.objects.filter(user=request.user).order_by('-order_date')
    paginator = Paginator(user_orders, 10)  # 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'order_history.html', {'page_obj': page_obj})





def copy(request):
    return render(request, 'copy.html')


def index(request):
    return render(request, 'index.html')


def contact(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(username=username,email=email,subject=subject,message=message)
        contact.save()
    return render(request, 'contact.html')



# def shop(request, category_id=None):
#     categories = Category.objects.all()
#     category_id = request.GET.get('category')
#
#     if category_id:
#         products = Product.objects.filter(category=category_id)
#     else:
#         products = Product.objects.all()
#
#     paginator = Paginator(products, 6)  # 6 products per page(pagination)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'shop.html', {'products': page_obj, 'categories': categories, 'paginator': paginator})
#

def shop(request, category_id=None):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    query = request.GET.get('q')  # Get the search query

    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()

    if query:  # If a search query is present
        products = products.filter(name__icontains=query)  # Filter products by name

    paginator = Paginator(products, 6)  # 6 products per page (pagination)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {
        'products': page_obj,
        'categories': categories,
        'paginator': paginator,
        'query': query  # Pass the query to the template
    })




def cart(request):
    return render(request, 'cart.html')


def signup(request):
    if request.method == "POST":

        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "username is already exist! please enter other username")
            return redirect('index')
        # if User.objects.filter(email=email):
        #     messages.error(request,"email already registered !")
        #     return redirect('signup')

        if len(username) > 10:
            messages.error(request, "username must be under 10 character")
        if pass1 != pass2:
            messages.error(request, "password did not match!")
        if not username.isalnum():
            messages.error(request, "username must be alpha-numeric!")

            return redirect('index')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)

        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been created \n email sent to your account !!")

        return redirect('signin')

    return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":

        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'index.html', {'fname': fname})

        else:
            messages.error(request, "wrong pass!")
            return redirect('index')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully...!!")
    return redirect('index')



def detail(request, pk):
    products = Product.objects.all()
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'detail.html', {'product': product,'products':products})


# CART

def add_cart(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user
    cart_item, created = AddItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


def view_cart(request):
    cart_items = AddItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping_charge = 50
    total = subtotal + shipping_charge
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'subtotal': subtotal, 'total': total,'shipping_charge':shipping_charge})




def checkout(request):
    if request.method == 'POST':
        # Get the checkout form data
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        number = request.POST['number']
        add1 = request.POST['add1']
        add2 = request.POST['add2']
        country = request.POST['country']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']

        # Calculate the total
        cart_items = AddItem.objects.filter(user=request.user)
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping_charge = 50
        total = subtotal + shipping_charge

        # Create an order instance
        order = OrderDetail(
            user=request.user,
            total=total,
            quantity=sum(item.quantity for item in cart_items),
        )
        order.save()


        # Create a Checkout
        checkout = Checkout(
            order=order,
            firstname=firstname,
            lastname=lastname,
            email=email,
            number=number,
            add1=add1,
            add2=add2,
            country=country,
            city=city,
            state=state,
            zipcode=zipcode,
        )
        checkout.save()

        # Update the order status to 'processing'
        order.status = 'processing'
        order.save()



        # Razorpay Payment Gateway Callback
        if request.POST.get('payment_id'):
            # Update the order status to 'paid'
            order.status = 'paid'
            order.save()

            # Display success message
            messages.success(request, 'Payment successful! You can now place the order.')



        # Clear the cart
        cart_items.delete()

        # Redirect to a success page
        # messages.success(request, 'Order placed successfully!')
        return redirect('order_conf')
    else:
        cart_items = AddItem.objects.filter(user=request.user)
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping_charge = 50
        total = subtotal + shipping_charge

    return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_charge': shipping_charge,
            'total': total,
        })



def order_conf(request):
    return render(request, 'order_conf.html')



def remove_from_cart(request, pk):
    cart_item = AddItem.objects.get(id=pk)
    cart_item.delete()
    return redirect('view_cart')


def change_quantity(request, pk):
    cart_item = AddItem.objects.get(id=pk)
    quantity = request.POST.get('quantity')
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('view_cart')


# WISHLIST
def add_fav(request, pk):
    product = Product.objects.get(id=pk)
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favourite.delete()
    return redirect('fav')


def fav(request):
    favourites = Favourite.objects.filter(user=request.user)
    wishlist = [f.product for f in favourites]
    return render(request, 'fav.html', {'wishlist': wishlist})


def remove_fav(request, pk):
    favourites = Favourite.objects.get(id=pk)
    favourites.delete()
    return redirect('fav')
