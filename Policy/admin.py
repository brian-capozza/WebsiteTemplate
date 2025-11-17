from django.contrib import admin
from Policy.models import AboutUs, OurServices, PrivacyPolicy, TermsOfService, FAQ, ShippingPolicy, ReturnPolicy, PaymentOptions
from WebsiteTemplate.admin import admin_site

from WebsiteTemplate.settings import TOTP_ADMIN

# Register your models here.

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['about_us_id', 'used', 'about_us_text']

class OurServicesAdmin(admin.ModelAdmin):
    list_display = ['our_services_id', 'used', 'our_services_text']

class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['privacy_policy_id', 'used', 'privacy_policy_text']

class TermsOfServiceAdmin(admin.ModelAdmin):
    list_display = ['terms_of_service_id', 'used', 'terms_of_service_text']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['faq_id', 'used', 'faq_text']

class ShippingPolicyAdmin(admin.ModelAdmin):
    list_display = ['shipping_policy_id', 'used', 'shipping_policy_text']

class ReturnPolicyAdmin(admin.ModelAdmin):
    list_display = ['return_policy_id', 'used', 'return_policy_text']

class PaymentOptionsAdmin(admin.ModelAdmin):
    list_display = ['payment_options_id', 'used', 'payment_options_text']


if TOTP_ADMIN:
    admin_site.register(AboutUs, AboutUsAdmin)
    admin_site.register(OurServices, OurServicesAdmin)
    admin_site.register(PrivacyPolicy, PrivacyPolicyAdmin)
    admin_site.register(TermsOfService, TermsOfServiceAdmin)
    admin_site.register(FAQ, FAQAdmin)
    admin_site.register(ShippingPolicy, ShippingPolicyAdmin)
    admin_site.register(ReturnPolicy, ReturnPolicyAdmin)
    admin_site.register(PaymentOptions, PaymentOptionsAdmin)
else:
    admin.site.register(AboutUs, AboutUsAdmin)
    admin.site.register(OurServices, OurServicesAdmin)
    admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)
    admin.site.register(TermsOfService, TermsOfServiceAdmin)
    admin.site.register(FAQ, FAQAdmin)
    admin.site.register(ShippingPolicy, ShippingPolicyAdmin)
    admin.site.register(ReturnPolicy, ReturnPolicyAdmin)
    admin.site.register(PaymentOptions, PaymentOptionsAdmin)