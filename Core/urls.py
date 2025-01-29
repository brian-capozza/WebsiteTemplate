from django.urls import path, include
from Core.views import index, order_list_view, order_detail_view, product_list_view, category_list_view, category_product_list_view, product_detail_view, add_to_cart, cart_view, delete_item_from_cart, refresh_cart, checkout_view, payment_completed_view, payment_failed_view, stripe_webhook, generation_list_view, generation_product_list_view
from Core.views import CreateCheckoutSessionView

app_name = 'Core'


urlpatterns = [
    # Homepage
    path('', index, name='index'),

    path('shop/', product_list_view, name='product-list'),
    path('shop/<pid>', product_detail_view, name='product-detail'),

    # Category
    path('category/', category_list_view, name='category-list'),
    path('category/<title>/', category_product_list_view, name='category-product-list'),

    # Generation
    path('generation/', generation_list_view, name='generation-list'),
    path('generation/<title>/', generation_product_list_view, name='generation-product-list'),

    # Cart
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', cart_view, name='cart'),

    # Delete Item From Cart
    path('delete-from-cart/', delete_item_from_cart, name='delete-from-cart'),

    # Refresh Cart
    path('refresh-cart/', refresh_cart, name='refresh-cart'),

    # Checkout
    path('checkout/', checkout_view, name='checkout'),

    # Stripe
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),

    path('payment-completed/', payment_completed_view, name='payment-completed'),
    path('payment-failed/', payment_failed_view, name='payment-failed'),

    # Orders
    path('orders/', order_list_view, name='order-list'),
    path('orders/<oid>', order_detail_view, name='order-detail'),
]