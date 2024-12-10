import razorpay
from django.conf import settings

def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_order(amount, currency="INR", payment_capture=1):
    client = get_razorpay_client()
    order_data = {
        'amount': amount * 100,  # Amount is in paise
        'currency': currency,
        'payment_capture': payment_capture
    }
    return client.order.create(data=order_data)

def verify_payment(payment_id, order_id, signature):
    client = get_razorpay_client()
    try:
        # Razorpay verifies the signature
        client.utility.verify_payment_signature({
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        })
        return True
    except:
        return False

