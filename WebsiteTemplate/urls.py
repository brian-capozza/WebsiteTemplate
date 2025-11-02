"""
URL configuration for WebsiteTemplate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# TOTP Import/Setup
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

# Authentication App 
from Authentication.models import CustomUser
from Authentication.admin import CustomUserAdmin

# Core App
from Core.models import Product, Category, Generation, Vendor, Order, ProductReview, Wishlist
from Core.admin import ProductAdmin, CategoryAdmin, GenerationAdmin, VendorAdmin, OrderAdmin, ProductReviewAdmin, WishlistAdmin

# Policy App
from Policy.models import AboutUs, OurServices, PrivacyPolicy, TermsOfService, FAQ, ShippingPolicy, ReturnPolicy, PaymentOptions
from Policy.admin import AboutUsAdmin, OurServicesAdmin, PrivacyPolicyAdmin, TermsOfServiceAdmin, FAQAdmin, ShippingPolicyAdmin, ReturnPolicyAdmin, PaymentOptionsAdmin

# Switch App
from Switch.models import ProductionSwitch
from Switch.admin import ProductionSwitchAdmin

class OTPAdmin(OTPAdminSite):
    pass
    
admin_site = OTPAdmin(name='OTPAdmin')

#admin_site.register(TOTPDevice, TOTPDeviceAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Generation, GenerationAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)

admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(OurServices, OurServicesAdmin)
admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
admin.site.register(TermsOfService, TermsOfServiceAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(ShippingPolicy, ShippingPolicyAdmin)
admin.site.register(ReturnPolicy, ReturnPolicyAdmin)
admin.site.register(PaymentOptions, PaymentOptionsAdmin)

admin.site.register(ProductionSwitch, ProductionSwitchAdmin)

#admin_site.register(CustomUser, CustomUserAdmin)
#admin_site.register(Product, ProductAdmin)
#admin_site.register(Category, CategoryAdmin)
#admin_site.register(Generation, GenerationAdmin)
#admin_site.register(Vendor, VendorAdmin)
#admin_site.register(Order, OrderAdmin)
#admin_site.register(ProductReview, ProductReviewAdmin)
#admin_site.register(Wishlist, WishlistAdmin)

#admin_site.register(AboutUs, AboutUsAdmin)
#admin_site.register(OurServices, OurServicesAdmin)
#admin_site.register(PrivacyPolicy, PrivacyPolicyAdmin)
#admin_site.register(TermsOfService, TermsOfServiceAdmin)
#admin_site.register(FAQ, FAQAdmin)
#admin_site.register(ShippingPolicy, ShippingPolicyAdmin)
#admin_site.register(ReturnPolicy, ReturnPolicyAdmin)
#admin_site.register(PaymentOptions, PaymentOptionsAdmin)

#admin_site.register(ProductionSwitch, ProductionSwitchAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('apollo/', admin_site.urls),
    path('', include('Core.urls')),
    path('user/', include('Authentication.urls')),
    path('policy/', include('Policy.urls')),
    #path('switch/', include('Switch.urls')), No urls currently
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)