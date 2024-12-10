from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .services.razorpay_service import create_order, verify_payment
from .models import Payment



def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products":cart_products,"quantities":quantities,"totals":totals})

def cart_product(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    return render(request, "cart_summary.html", {"cart_products":cart_products,"quantities":quantities})

    
def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		#get cart quantity
		cart_quantity = cart.__len__()
  
		# Return resonse
		cart.add(product=product,quantity=product_qty)
		response = JsonResponse({'qty :': cart_quantity})
		messages.success(request, ("Item Added to Shopping Cart..."))
		return response

 
 
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        
        response = JsonResponse({'product':product_id})
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

# def pay(request):
#     cart = Cart(request)
#     totals = cart.cart_total()
#     return render(request, "pay.html",{"totals":totals})


def pay(request):
    cart = Cart(request)
    
    if request.method == "POST":
        amount = float(request.POST['amount'])
        order = create_order(amount)  
        total = cart.cart_total()  
        
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': total * 100,  # Amount in paise for Razorpay
            'currency': order['currency'],
            'totals': total, 
        }
        return render(request, 'payments/checkout.html', context)
    
    cart = Cart(request)
    total = cart.cart_total() 
    context = {
        'totals': total,  
    }
    return render(request, 'payments/pay.html', context)


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Verify the payment
        if verify_payment(payment_id, order_id, signature):
            # save to database
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=1000,  # You can store actual amount from order
                status='Success'
            )
            messages.success(request, ("Payment Success Thank you for your purchasing!"))
            return render(request, 'cart_summary.html')

        else:
            # Payment failed
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=1000,
                status='Failed'
            )
            messages.success(request, ("Payment Failed please try again later"))
            return render(request, 'cart_summary.html')
    return redirect('pay')
