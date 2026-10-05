from django.views.generic import ListView
from django.db.models import Count, Q
from .models import Category, Product

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        # Base query optimized with select_related
        queryset = Product.objects.select_related('category').filter(product_is_available=True)
        
        # ----------------------------------------------------
        # Step 1: Search Logic using Q Objects
        # ----------------------------------------------------
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(product_title__icontains=q) | Q(product_description__icontains=q)
            )

        # ----------------------------------------------------
        # Step 2: Faceted Filter Controls
        # ----------------------------------------------------
        category_id = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        in_stock = self.request.GET.get('in_stock')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price:
            queryset = queryset.filter(product_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(product_price__lte=max_price)
        if in_stock == 'true':
            queryset = queryset.filter(product_stock__gt=0)

        # ----------------------------------------------------
        # Step 3: Sorting Mechanisms
        # ----------------------------------------------------
        sort_by = self.request.GET.get('sort', 'newest')
        sort_mapping = {
            'price_asc': 'product_price',
            'price_desc': '-product_price',
            'newest': '-created_at',
            'popularity': '-created_at',  # Default fallback
        }
        ordering = sort_mapping.get(sort_by, '-created_at')

        return queryset.order_by(ordering)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Categories with annotated active product count
        context["categories"] = Category.objects.annotate(
            total_products=Count("products", filter=Q(products__product_is_available=True))
        )
        return context