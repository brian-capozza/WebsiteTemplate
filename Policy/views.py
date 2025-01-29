from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Core.views import conditional_login_required
from Policy.models import AboutUs, OurServices, PrivacyPolicy, TermsOfService, FAQ, ShippingPolicy, ReturnPolicy, PaymentOptions

# Create your views here.

@conditional_login_required(login_required)
def about_us_view(request):
    try:
        about_us_text = AboutUs.objects.get(used=True)

        context = {
            'about_us_text': about_us_text
        }
        return render(request, 'Policy/about-us.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')

@conditional_login_required(login_required)
def our_services_view(request):
    try:
        our_services_text = OurServices.objects.get(used=True)

        context = {
            'our_services_text': our_services_text
        }
        return render(request, 'Policy/our-services.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')

@conditional_login_required(login_required)
def privacy_policy_view(request):
    try:
        privacy_policy_text = PrivacyPolicy.objects.get(used=True)

        context = {
            'privacy_policy_text': privacy_policy_text
        }
        return render(request, 'Policy/privacy-policy.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')

@conditional_login_required(login_required)
def terms_of_service_view(request):
    try:
        terms_of_service_text = TermsOfService.objects.get(used=True)

        context = {
            'terms_of_service_text': terms_of_service_text
        }
        return render(request, 'Policy/terms-of-service.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')

@conditional_login_required(login_required)
def faq_view(request):
    try:
        faq_text = FAQ.objects.get(used=True)

        context = {
            'faq_text': faq_text
        }
        return render(request, 'Policy/faq.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')

@conditional_login_required(login_required)
def shipping_policy_view(request):
    try:
        shipping_policy_text = ShippingPolicy.objects.get(used=True)

        context = {
            'shipping_policy_text': shipping_policy_text
        }
        return render(request, 'Policy/shipping-policy.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')

@conditional_login_required(login_required)
def return_policy_view(request):
    try:
        return_policy_text = ReturnPolicy.objects.get(used=True)
        print(return_policy_text)

        context = {
            'return_policy_text': return_policy_text
        }
        return render(request, 'Policy/return-policy.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')

@conditional_login_required(login_required)
def payment_options_view(request):
    try:
        payment_options_text = PaymentOptions.objects.get(used=True)

        context = {
            'payment_options_text': payment_options_text
        }
        return render(request, 'Policy/payment-options.html', context=context)
    except:
        return render(request, 'Policy/unavailable.html')