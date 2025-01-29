from django.db import models
from shortuuid.django_fields import ShortUUIDField
from tinymce.models import HTMLField
from django.db.models import UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _

# Create your models here.

class AboutUs(models.Model):
    about_us_id = ShortUUIDField(unique=True, length=10, max_length=15, prefix='about', alphabet='0123456789')
    about_us_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'About Us'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_about'),
        ]

    def __str__(self):
        return 'About Us'
    
#======================================================================================= 

class OurServices(models.Model):
    our_services_id = ShortUUIDField(unique=True, length=10, max_length=17, prefix='service', alphabet='0123456789')
    our_services_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'Our Services'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_service'),
        ]

    def __str__(self):
        return 'Our Services'
    
#======================================================================================= 

class PrivacyPolicy(models.Model):
    privacy_policy_id = ShortUUIDField(unique=True, length=10, max_length=17, prefix='privacy', alphabet='0123456789')
    privacy_policy_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'Privacy Policy'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_privacy_policy'),
        ]

    def __str__(self):
        return 'Privacy Policy'
    
#======================================================================================= 

class TermsOfService(models.Model):
    terms_of_service_id = ShortUUIDField(unique=True, length=10, max_length=15, prefix='terms', alphabet='0123456789')
    terms_of_service_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'Terms of Service'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_terms_of_service'),
        ]

    def __str__(self):
        return 'Terms of Service'

#======================================================================================= 

class FAQ(models.Model):
    faq_id = ShortUUIDField(unique=True, length=10, max_length=13, prefix='faq', alphabet='0123456789')
    faq_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'FAQ'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_faq'),
        ]

    def __str__(self):
        return 'FAQ'
    
#======================================================================================= 

class ShippingPolicy(models.Model):
    shipping_policy_id = ShortUUIDField(unique=True, length=10, max_length=18, prefix='shipping', alphabet='0123456789')
    shipping_policy_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'Shipping Policy'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_shipping_policy'),
        ]

    def __str__(self):
        return 'Shipping Policy'
    
#======================================================================================= 

class ReturnPolicy(models.Model):
    return_policy_id = ShortUUIDField(unique=True, length=10, max_length=16, prefix='return', alphabet='0123456789')
    return_policy_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'Return Policy'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_return_policy'),
        ]

    def __str__(self):
        return 'Return Policy'
    
#======================================================================================= 

class PaymentOptions(models.Model):
    payment_options_id = ShortUUIDField(unique=True, length=10, max_length=17, prefix='payment', alphabet='0123456789')
    payment_options_text = HTMLField()
    used = models.BooleanField(_('Is Used'), default=False)

    class Meta:
        verbose_name_plural = 'Payment Options'
        constraints = [
            UniqueConstraint(fields=['used'], condition=Q(used=True), name='one_text_per_payment_options'),
        ]

    def __str__(self):
        return 'Payment Options'