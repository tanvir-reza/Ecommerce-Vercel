# We will use this function to generate a random order id for the order
from .models import Order
from store.models import Product
import random, string
import requests

def generate_unique_id():
    length = 5
    while True:
        order_id = 'ODR' + ''.join(random.choices(string.digits, k=length))
        if Order.objects.filter(order_id=order_id).count() == 0:
            break
    return order_id

def tnx_genarator():
    length = 10
    while True:
        tnx_id = ''.join(random.choices(string.digits, k=length))
        if Order.objects.filter(tnx_id=tnx_id).count() == 0:
            break
    return tnx_id

# We will use this function to generate a random order id for the order
def cart(request):
    cart = request.session.get('cart', {})
    product_price = 0
    cart_items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        product_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity})
    return {'cart_items': cart_items,'product_price':product_price}



def sendMessage(name,phone,order_id,total_ammount,payment_type):
    api = 'dTUsZl0CvtmvDF35kQY1'
    rec = phone
    msg = f"Dear {name}, \nYour Order ID: {order_id} and Total Ammount: {total_ammount} payment by {payment_type} \nOrder Confirmed. \nThank You For Shopping With Us."
    response = requests.post('http://bulksmsbd.net/api/smsapi?api_key='+api+'&type=text&number='+rec+'&senderid=8809617611061&message='+msg+'').json()
    print(response)
    return True