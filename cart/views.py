from django.shortcuts import render
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.urls import reverse
from django.views import generic
from django.core import cache
from store.models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .helpers import generate_unique_id,tnx_genarator
from .models import Order,OrderItem
import datetime
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .helpers import sendMessage



def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('prod_id')
        qunatity = int(request.POST.get('qty'))
        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id] += qunatity
        else:
            cart[product_id] = qunatity
        request.session['cart'] = cart
        length = len(cart)
        print(cart)
        return JsonResponse({'length':length})
    
@csrf_exempt
def cart_del(request):
    if request.POST:
        product_id = request.POST.get('prod_id')
        print(product_id)
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
        request.session['cart'] = cart
        length = len(cart)
        return JsonResponse({'length':length})
        


def cart_summery(request):
    cart = request.session.get('cart', {})
    product_price = 0
    cart_items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        product_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity})
    length = len(cart_items)
    print(product_price)
    return render(request, 'cart/cart-summary.html', {'cart_items': cart_items,'product_price':product_price,'length':length})

@login_required(login_url='login')
def checkout(request):
    user = Profile.objects.filter(user=request.user).first()
    if user is not None:
        print("ami")
        if user.name == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
        if user.phone == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
    cart = request.session.get('cart', {})
    user = request.user
    product_price = 0
    cart_items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        product_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity})

    return render(request, 'cart/checkout.html',{'cart_items': cart_items,'product_price':product_price,'user':user})


@login_required(login_url='login')
def payment(request):
    user = Profile.objects.filter(user=request.user).first()
    
    if user is not None:
        if user.name == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
        if user.phone == "":
            messages.error(request, 'Please Update Your Profile')
            return redirect('update_profile')
        
    
    if request.method == 'POST':
        status = 'https://narsten.com/cart/payment-status/'
        if request.POST.get('payment') == 'ssl':
            order_id = generate_unique_id()
            user = request.user
            tran_id = tnx_genarator()
            payment_type = 'SSL COMMERZ'
            cart = request.session.get('cart', {})
            total_ammount = 0
            cart_items = []
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                total_ammount += product.price * quantity
                cart_items.append({'product': product, 'quantity': quantity})
            len(cart_items)

            del request.session['cart']
            
            profile = Profile.objects.get(user=user)
            name = profile.name
            phone = profile.phone
            shipping_address = request.POST.get('shipping_address').strip()
            
            
            invoice =  download_pdf(order_id,name,phone,shipping_address,tran_id,payment_type,total_ammount,cart_items)

            order = Order.objects.create(
                order_id=order_id,
                user=user,
                shipping_address=shipping_address,
                tnx_id=tran_id, 
                payment_status=False,
                payment_type=payment_type,
                invoice=invoice,
                total_amount=total_ammount,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    product=item['product'],
                    order=order,
                    quantity=item['quantity'],
                )
            order.save()


            # SSLCOMMERZ Start
            from sslcommerz_lib import SSLCOMMERZ 
            settings = { 'store_id': 'abc6574d69b71365', 'store_pass': 'abc6574d69b71365@ssl', 'issandbox': True }
            sslcz = SSLCOMMERZ(settings)
            post_body = {}
            post_body['total_amount'] = total_ammount
            post_body['currency'] = "BDT"
            post_body['tran_id'] = tran_id
            post_body['success_url'] = status
            post_body['fail_url'] = status
            post_body['cancel_url'] = status
            post_body['emi_option'] = 0
            post_body['cus_name'] = name
            post_body['cus_email'] = "test@test.com"
            post_body['cus_phone'] = phone
            post_body['cus_add1'] = shipping_address
            post_body['cus_city'] = "Dhaka"
            post_body['cus_country'] = "Bangladesh"
            post_body['shipping_method'] = "NO"
            post_body['multi_card_name'] = ""
            post_body['num_of_item'] = len(cart_items)
            post_body['product_name'] = "Test"
            post_body['product_category'] = "Test Category"
            post_body['product_profile'] = "general"

            response = sslcz.createSession(post_body) # API response
            print(response)
            
            return redirect(response['GatewayPageURL'])
        
        if request.POST.get('payment') == 'cash':
            order_id = generate_unique_id()
            user = request.user
            tran_id = '00'
            payment_type = 'CASH ON DELIVERY'
            cart = request.session.get('cart', {})
            total_ammount = 0
            cart_items = []
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                total_ammount += product.price * quantity
                cart_items.append({'product': product, 'quantity': quantity})
            len(cart_items)
            
            profile = Profile.objects.get(user=user)
            name = profile.name
            phone = profile.phone
            shipping_address = profile.address
            
            
            invoice =  download_pdf(order_id,name,phone,shipping_address,tran_id,payment_type,total_ammount,cart_items)

            order = Order.objects.create(
                order_id=order_id,
                user=user,
                shipping_address=shipping_address,
                tnx_id=tran_id, 
                payment_status=True,
                payment_type=payment_type,
                invoice=invoice,
                total_amount=total_ammount,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    product=item['product'],
                    order=order,
                    quantity=item['quantity'],
                )
            order.save()
            del request.session['cart']
            messages.error(request, 'Order Confirmed')
            sendMessage(name,phone,order_id,total_ammount,payment_type)
            return redirect('profile')

        
    return redirect('checkout')

@csrf_exempt
def payment_status(request):
    if request.method == 'POST':
        payment_data = request.POST
        print(payment_data)
        if payment_data['status'] == 'VALID':
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']

            Order.objects.filter(tnx_id=tran_id).update(payment_status=True,val_id=val_id)
            orderrid = Order.objects.filter(tnx_id=tran_id).first()
            order_id = orderrid.order_id
            total = orderrid.total_amount
            payment_type = payment_data['card_issuer']
            user = orderrid.user
            profile = Profile.objects.get(user=user)
            name = profile.name
            phone = profile.phone
            sendMessage(name,phone,order_id,total,payment_type)
            messages.error(request, 'Order Confirmed')
            return redirect('profile')
        else:
            return redirect('payment_fail')
        

    

def payment_success(request):
    
    pass

    

def payment_fail(request):
    messages.error(request, 'Payment Failed')
    return redirect('profile')


    

# PDF GENERATOR
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import os



# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     print(html)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,encoding='ISO-8859-1')
#     print(pdf)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

def download_pdf(order_id,name,phone,shipping_address,tran_id,payment_type,total_ammount,cart_items):
    time = datetime.datetime.now()

    context = {
        'cart_items': cart_items,
        'total_price':total_ammount,
        'payment':payment_type,
        'pdf_version': True,
        'order_id':order_id,
        'tran_id':tran_id,
        'time':time,
        'name':name,
        'phone':phone,
        'shipping_address':shipping_address,

    }
    # Create a Django response object, and specify content_type as pdf
    template_path = 'cart/pdf.html'
    response = BytesIO()
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    response.seek(0)

    pdf_data = response.getvalue()

    pdf = ContentFile(pdf_data, name='order-' + order_id + '.pdf')

    return pdf

