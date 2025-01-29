from django.db import models

# Create your models here.

from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from Authentication.models import CustomUser
from tinymce.models import HTMLField
from django.db.models import UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _


STATUS_CHOICE = (
    ('packing', 'Packing'),
    ('packed', 'Packed'),
    ('label_made', 'Label Made'),
    ('shipped', 'Shipped')
)

STATUS = (
    ('drafts', 'Drafts'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
    ('sold_out', 'Sold Out')
)

PRODUCTION_SWITCH = (
    ('locked', 'Locked'),
    ('production', 'Production'),
    ('testing', 'Testing'),
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Generation(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='gen', alphabet='abcdefgh')
    title = models.CharField(max_length=100, default='')
    order = models.IntegerField(default='1')

    class Meta:
        verbose_name_plural = 'Generations'
        ordering = ['order']

    def __str__(self):
        return self.title


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet='abcdefgh')
    title = models.CharField(max_length=100, default='')
    generation = models.ManyToManyField(Generation)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    

#class Tags(models.Model):
#    pass
    

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet='abcdefgh')

    title = models.CharField(max_length=100, default='CatOnTheRoof')
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = HTMLField(null=True, blank=True, default='I am a Vendor')

    address = models.CharField(max_length=100, default='123 Main Street')
    contact = models.CharField(max_length=100, default='860-555-5050')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" >')

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='prd', alphabet='abcdefgh')

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    generation = models.ForeignKey(Generation, on_delete=models.SET_NULL, null=True)
    
    title = models.CharField(max_length=100, default='Beyblade')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = HTMLField(null=True, blank=True, default='This is the product')

    price = models.DecimalField(max_digits=999, decimal_places=2, default='99.99')
    old_price = models.DecimalField(max_digits=999, decimal_places=2, default='199.99')
    quantity = models.IntegerField(default='1')

    specifications = HTMLField(null=True, blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.CASCADE)

    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix='sku', alphabet='0123456789')

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" >')

    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to='products-images', default='product.jpg')
    product = models.ForeignKey(Product, related_name='p_images', on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'



#=================================================================================
        
class Order(models.Model):
    order_id = ShortUUIDField(unique=True, length=25, max_length=30, prefix='ord', alphabet='0123456789')
    order_number = models.CharField(max_length=200, default='ORDER_NUMBER-0', editable=False)
    order_price = models.DecimalField(max_digits=999, decimal_places=2, default='0', editable=False)
    order_date = models.DateField(auto_now_add=True, editable=False)
    order_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default='packing')
    tracking_number = models.CharField(max_length=50, default='', blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True, editable=False)
    address = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name_plural = 'Orders'

class OrderItems(models.Model):
    pid = ShortUUIDField(length=10, max_length=20, prefix='prd', alphabet='abcdefgh', editable=False)
    title = models.CharField(max_length=100, default='Beyblade', editable=False)
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg', editable=False)
    price = models.DecimalField(max_digits=999, decimal_places=2, default='99.99', editable=False)
    quantity = models.IntegerField(default='1', editable=False)
    total_price = models.DecimalField(max_digits=999, decimal_places=2, default='0.00', editable=False)

    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Order Items'

class ShippingAddress(models.Model):
    address_line_one = models.CharField(max_length=100, null=True)
    address_line_two = models.CharField(max_length=100, null=True)
    address_city = models.CharField(max_length=100, null=True)
    address_zip_code = models.CharField(max_length=100, null=True)
    address_state = models.CharField(max_length=100, null=True)
    address_country = models.CharField(max_length=100, null=True)

    order = models.ForeignKey(Order, related_name='order_ship_address', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Shipping Address'

class BillingAddress(models.Model):
    address_line_one = models.CharField(max_length=100, null=True)
    address_line_two = models.CharField(max_length=100, null=True)
    address_city = models.CharField(max_length=100, null=True)
    address_zip_code = models.CharField(max_length=100, null=True)
    address_state = models.CharField(max_length=100, null=True)
    address_country = models.CharField(max_length=100, null=True)

    order = models.ForeignKey(Order, related_name='order_bill_address', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Billing Address'

#=======================================================================================
    

class ProductReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title