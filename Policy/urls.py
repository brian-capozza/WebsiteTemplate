from django.urls import path, include
from Policy.views import about_us_view, our_services_view, privacy_policy_view, terms_of_service_view, faq_view, shipping_policy_view, return_policy_view, payment_options_view

app_name = 'Policy'

urlpatterns = [
    path('about-us/', about_us_view, name='about-us'),
    path('our-services/', our_services_view, name='our-services'),
    path('privacy-policy/', privacy_policy_view, name='privacy-policy'),
    path('terms-of-service/', terms_of_service_view, name='terms-of-service'),
    path('faq/', faq_view, name='faq'),
    path('shipping-policy/', shipping_policy_view, name='shipping-policy'),
    path('return-policy/', return_policy_view, name='return-policy'),
    path('payment-options/', payment_options_view, name='payment-options'),
]