from django.contrib import admin
from Core.models import Product, Category, Vendor, Wishlist, ProductImages, ProductReview, ShippingAddress, BillingAddress
from Core.models import Order, OrderItems

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'featured', 'product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class GenerationAdmin(admin.ModelAdmin):
    list_display = ['title']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']


class OrderItemsAdmin(admin.TabularInline):
    model = OrderItems
    extra = 0
    readonly_fields = ['title', 'image', 'price', 'quantity']

class ShippingAddressAdmin(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    readonly_fields = ['order', 'address_line_one', 'address_line_two', 'address_city', 'address_zip_code', 'address_state', 'address_country']

class BillingAddressAdmin(admin.StackedInline):
    model = BillingAddress
    extra = 0
    readonly_fields = ['order', 'address_line_one', 'address_line_two', 'address_city', 'address_zip_code', 'address_state', 'address_country']

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsAdmin, ShippingAddressAdmin, BillingAddressAdmin]
    list_display = ['order_number', 'order_price', 'order_date', 'order_status', 'tracking_number', 'address']
    list_editable = ['order_status', 'tracking_number']
    readonly_fields = ['order_number', 'order_price', 'order_date', 'customer_email']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']