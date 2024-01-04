

def cartCount(request):
    cart = request.session.get('cart')
    
    if cart:
        return {'cart_count': len(cart)}
    else:
        return {'cart_count': 0}
    
