from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, size=None, color=None, price_increment=0):
        product_id = str(product.id)
        cart_key = f"{product_id}-{size}-{color}" if (size or color) else product_id
        
        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product_id,
                'quantity': 0,
                'price': str(product.product_price),
                'size': size,
                'color': color,
                'price_increment': str(price_increment)
            }

        if override_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_key):
        """Remove item using its session key (cart_key or product_id)"""
        product_key = str(product_key)
        if product_key in self.cart:
            del self.cart[product_key]
            self.save()

    def __iter__(self):
    # Retrieve all unique product IDs (handles standard product_id keys or composite keys)
        product_ids = [
            item.get('product_id', key.split('-')[0]) 
            for key, item in self.cart.items()
        ]
        products = Product.objects.filter(id__in=product_ids)
        
        # Create lookup map for fetched product objects
        product_map = {str(product.id): product for product in products}

        for key, item in self.cart.items():
            # Resolve target product ID from item dict or key
            p_id = str(item.get('product_id', key.split('-')[0]))
            
            # Safely skip item if product no longer exists in database
            if p_id not in product_map:
                continue

            # Shallow copy item dict to preserve session immutability
            item_data = item.copy()
            item_data['key'] = key  # Expose the session key to the template
            item_data['product'] = product_map[p_id]

            base_price = Decimal(str(item_data.get('price', '0')))
            price_increment = Decimal(str(item_data.get('price_increment', '0')))

            item_data['unit_price'] = base_price + price_increment
            item_data['total_price'] = item_data['unit_price'] * item_data['quantity']

            yield item_data

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()