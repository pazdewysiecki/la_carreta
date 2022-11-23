#Carrito

from math import prod


class Cart():
    def __init__(self,request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self,product):
        id = str(product.id)
        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                "product_id": product.id,
                "name": product.name,
                "quantity": 1,
                "price": product.price,
                "image": product.image.url,
                "excerpt": product.excerpt,
                "category": product.category_id,  
                #"cantidad": product.cantidad,
                "unidad_medida": product.unidadmedida_id,
            }
        else:
            self.cart[id]["quantity"] += 1
            self.cart[id]["price"] += product.price
        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self,product):
            for key, value in self.cart.items():
                if key == str(product.id):
                    value["quantity"] = value["quantity"] - 1
                    value["price"] = value["price"] - product.price
                    if value["quantity"] < 1:
                        self.remove(product)
                    else:
                        self.save()
                    break
                else:
                    print("El producto no existe en el carrito")

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True
    
    