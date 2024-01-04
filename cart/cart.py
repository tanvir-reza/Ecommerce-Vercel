# from django.conf import settings
# from store.models import Product



# class Cart():

#     def __init__(self, request)->None:
#         """
#         Initialize the cart.
#         """
#         self.session = request.session
#         self.cart_id = settings.CART_ID
#         cart = self.session.get(self.cart_id)
#         self.cart = self.session[self.cart_id] = cart if cart else {}

#     def update(self,product_id,quantity=1):
#         product = Product.objects.get(id=product_id)
#         self.session[self.cart_id].setdefault(str(product_id),{'quantity':0,'price':str(product.price)})
#         updated_quantity = self.session[self.cart_id][str(product_id)]['quantity'] + quantity
#         self.session[self.cart_id][str(product_id)]['quantity'] = updated_quantity

#         if updated_quantity < 1:
#             del self.session[self.cart_id][str(product_id)]

#         self.save()



#     def __iter__(self):
#         """
#         Iterate over the items in the cart and get the products
#         from the database.
#         """
#         # get the product objects and add them to the cart
#         products = Product.objects.filter(id__in=list(self.cart.keys()))

#         cart = self.cart.copy()

#         for item in products:
#             product = Product.objects.get(id=item.id)
#             cart[str(item.id)]['product'] = {
#                 'id': item.id,
#                 'name': item.name,
#                 'price': item.price,
#                 'category': item.category,
#             }

#             yield item[str(item.id)]

#     def save(self):
#         self.session.modified = True

#     def __len__(self):
#         return len(list(self.cart.keys()))


# #     # def add(self, product, quantity=1, update_quantity=False):
# #     #     """
# #     #     Add a product to the cart or update its quantity.
# #     #     """
# #     #     product_id = str(product.id)

# #     #     if product_id not in self.cart:
# #     #         self.cart[product_id] = {'quantity': 0,
# #     #                                  'price': str(product.price)}

# #     #     if update_quantity:
# #     #         self.cart[product_id]['quantity'] = quantity

# #     #     else:
# #     #         self.cart[product_id]['quantity'] += quantity

# #     #     self.save()


# #     # def save(self):
# #     #     # update the session cart
# #     #     self.session[settings.CART_SESSION_ID] = self.cart
# #     #     # mark the session as "modified" to make sure it is saved
# #     #     self.session.modified = True


# #     # def remove(self, product):
# #     #     """
# #     #     Remove a product from the cart.
# #     #     """
# #     #     product_id = str(product.id)

# #     #     if product_id in self.cart:
# #     #         del self.cart[product_id]
# #     #         self.save()


# #     # def __iter__(self):
# #     #     """
# #     #     Iterate over the items in the cart and get the products
# #     #     from the database.
# #     #     """
# #     #     product_ids = self.cart.keys()

# #     #     # get the product objects and add them to the cart
# #     #     products = Product.objects.filter(id__in=product_ids)

# #     #     cart = self.cart.copy()

# #     #     for product in products:
# #     #         cart[str(product.id)]['product'] = product

# #     #     for item in cart.values():
# #     #         item['price'] = float(item['price'])
# #     #         item['total_price'] = item['price'] * item['quantity']

# #     #         yield item


# #     # def __len__(self):
# #     #     """
# #     #     Count all items in the cart.
# #     #     """
# #     #     return sum(item['quantity'] for item in self.cart.values())


# #     # def get_total_price(self):
# #     #     return sum(float(item['price']) * item['quantity'] for item in self.cart.values())


# #     # def clear(self):
# #     #     # remove cart from session
# #     #     del self.session[settings.CART_SESSION_ID]
# #     #     self.session.modified = True