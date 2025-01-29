from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from Core.models import Product, Category, Vendor, Wishlist, ProductImages, ProductReview, Order, OrderItems, ShippingAddress, BillingAddress, Generation
from Switch.models import ProductionSwitch
from Authentication.models import CustomUser
from django.template.loader import render_to_string
from django.views import View
from django.core.mail import send_mail
import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from paypal.standard.forms import PayPalPaymentsForm
from django.core.signals import request_finished
from django.template import RequestContext

stripe.api_key = settings.STRIPE_SECRET_KEY

def conditional_login_required(dec):
    def decorator(func):
        try:
            website_production = ProductionSwitch.objects.all()[0].production_switch
            if website_production == 'production':
                # Return the function unchanged, not decorated.
                return func
            elif website_production in ('locked', 'testing'):
                return dec(func)
            else:
                return dec(func)
        except:
            return dec(func)
    return decorator

def conditional_login_required_index(dec):
    def decorator(func):
        try:
            website_production = ProductionSwitch.objects.all()[0].production_switch
            if website_production in ('production', 'locked'):
                # Return the function unchanged, not decorated.
                return func
            elif website_production == 'testing':
                return dec(func)
            else:
                return dec(func)
        except:
            return dec(func)
    return decorator

# Create your views here.

#@conditional_login_required_index(login_required)
def index(request):
    website_production = ProductionSwitch.objects.all()[0].production_switch
    print(website_production)
    if website_production =='locked':
        return render(request, 'Core/construction.html')
    elif website_production in ('production', 'testing'):
        #products = Product.objects.all().order_by('-id')
        products = Product.objects.filter(product_status='published', featured=True)

        context = {
            'products': products
        }
        return render(request, 'Core/index.html', context=context)
    else:
        return render(request, 'Core/construction.html')

@conditional_login_required(login_required)
def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'Core/category-list.html', context=context)

@conditional_login_required(login_required)
def category_product_list_view(request, title):
    category = Category.objects.get(title=title)
    generations = []
    for gen in category.generation.all():
        generations.append(gen)
    products = Product.objects.filter(product_status='published', generation__in=generations)

    context = {
        'category': category,
        'products': products
    }
    return render(request, 'Core/category-product-list.html', context=context)

@conditional_login_required(login_required)
def generation_list_view(request):
    generations = Generation.objects.all()

    context = {
        'generations': generations
    }
    return render(request, 'Core/generation-list.html', context=context)

@conditional_login_required(login_required)
def generation_product_list_view(request, title):
    generation = Generation.objects.get(title=title)
    products = Product.objects.filter(product_status='published', generation=generation)

    context = {
        'generation': generation,
        'products': products
    }
    return render(request, 'Core/generation-product-list.html', context=context)

@conditional_login_required(login_required)
def product_list_view(request):
    products = Product.objects.filter(product_status='published')

    context = {
        'products': products
    }
    return render(request, 'Core/product-list.html', context=context)

@conditional_login_required(login_required)
def product_detail_view(request, pid):
    products = Product.objects.get(pid=pid)

    p_images = products.p_images.all()

    context = {
        'p': products,
        'p_images': p_images
    }

    return render(request, 'Core/product-detail.html', context=context)


@conditional_login_required(login_required)
def add_to_cart(request):
    cart_product = {
        str(request.GET['id']): {
            'title': request.GET['title'],
            'qty': int(request.GET['qty']),  # Convert qty to integer
            'price': request.GET['price'],
            'image': request.GET['image'],
            'pid': request.GET['pid'],
            'total_price': round(float(request.GET['price']) * int(request.GET['qty']), 2),
            'max_qty': request.GET['max_qty'],
            'product_status': request.GET['product_status']
        }
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if str(request.GET['id']) in cart_data:
            # Update quantity if product already exists in cart
            cart_data[str(request.GET['id'])]['qty'] = int(request.GET['qty'])
            cart_data.update(cart_data)
        else:
            # Add new product to cart
            cart_data.update(cart_product)

        request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({'data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


@conditional_login_required(login_required)
def cart_view(request):
    cart_subtotal_amount = 0
    cart_tax_amount = 0
    cart_total_amount = 0
    item_sold_out = 'false'
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_subtotal_amount += int(item['qty']) * float(item['price'])
            cart_tax_amount += (int(item['qty']) * float(item['price'])) * 0.0635
            cart_total_amount += (int(item['qty']) * float(item['price'])) * 1.0635
            item['total_price'] = int(item['qty']) * float(item['price'])
            current_product = Product.objects.get(pid=item['pid'])
            item['max_qty'] = current_product.quantity
            if current_product.product_status == 'sold_out':
                item['product_status'] = 'sold_out'
                item_sold_out = 'true'

        context = {
            'cart_data': request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_subtotal_amount': round(cart_subtotal_amount, 2),
            'cart_tax_amount': round(cart_tax_amount, 2),
            'cart_total_amount': round(cart_total_amount, 2),
            'sold_out': item_sold_out,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        }

        return render(request, 'Core/cart-page.html', context=context)
    else:
        return redirect('Core:index')
    

@conditional_login_required(login_required)
def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_subtotal_amount = 0
    cart_tax_amount = 0
    cart_total_amount = 0
    item_sold_out = 'false'
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_subtotal_amount += int(item['qty']) * float(item['price'])
            cart_tax_amount += (int(item['qty']) * float(item['price'])) * 0.0635
            cart_total_amount += (int(item['qty']) * float(item['price'])) * 1.0635
            item['total_price'] = int(item['qty']) * float(item['price'])
            current_product = Product.objects.get(pid=item['pid'])
            item['max_qty'] = current_product.quantity
            if current_product.product_status == 'sold_out':
                item['product_status'] = 'sold_out'
                item_sold_out = 'true'

    cart_context = {
        'cart_data': request.session['cart_data_obj'], 
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_subtotal_amount': round(cart_subtotal_amount, 2),
        'cart_tax_amount': round(cart_tax_amount, 2),
        'cart_total_amount': round(cart_total_amount, 2),
        'sold_out': item_sold_out,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }

    cart_content = render(request, "Core/async/cart-list.html", cart_context)
    return JsonResponse({"data": cart_content.content.decode(), 'totalcartitems': len(request.session['cart_data_obj'])})

@conditional_login_required(login_required)
def refresh_cart(request):
    product_id = str(request.GET.get('id'))
    product_qty = str(request.GET.get('qty'))
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_subtotal_amount = 0
    cart_tax_amount = 0
    cart_total_amount = 0
    item_sold_out = 'false'
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_subtotal_amount += int(item['qty']) * float(item['price'])
            cart_tax_amount += (int(item['qty']) * float(item['price'])) * 0.0635
            cart_total_amount += (int(item['qty']) * float(item['price'])) * 1.0635
            item['total_price'] = int(item['qty']) * float(item['price'])
            current_product = Product.objects.get(pid=item['pid'])
            item['max_qty'] = current_product.quantity
            if current_product.product_status == 'sold_out':
                item['product_status'] = 'sold_out'
                item_sold_out = 'true'

    cart_context = {
        'cart_data': request.session.get('cart_data_obj', {}),
        'totalcartitems': len(request.session.get('cart_data_obj', {})),
        'cart_subtotal_amount': round(cart_subtotal_amount, 2),
        'cart_tax_amount': round(cart_tax_amount, 2),
        'cart_total_amount': round(cart_total_amount, 2),
        'sold_out': item_sold_out,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }

    cart_content = render(request, "Core/async/cart-list.html", cart_context)
    return JsonResponse({"data": cart_content.content.decode(), 'totalcartitems': len(request.session['cart_data_obj'])})


@conditional_login_required(login_required)
def checkout_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_total_amount += (int(item['qty']) * float(item['price'])) * 1.0635


    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECIEVER_EMAIL,
        'amount': cart_total_amount,
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("Core:paypal-ipn")}',
        'return_url': f'http://{host}{reverse("Core:payment-completed")}',
        'cancel_url': f'http://{host}{reverse("Core:payment-failed")}',
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    cart_subtotal_amount = 0
    cart_tax_amount = 0
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_subtotal_amount += int(item['qty']) * float(item['price'])
            cart_tax_amount += (int(item['qty']) * float(item['price'])) * 0.0635
            cart_total_amount += (int(item['qty']) * float(item['price'])) * 1.0635
            item['total_price'] = int(item['qty']) * float(item['price'])

        context = {
            'cart_data': request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_subtotal_amount': round(cart_subtotal_amount, 2),
            'cart_tax_amount': round(cart_tax_amount, 2),
            'cart_total_amount': round(cart_total_amount, 2),
            'paypal_payment_button': paypal_payment_button
        }

        return render(request, 'Core/checkout.html', context=context)

@conditional_login_required(login_required)
def payment_completed_view(request):
    cart_subtotal_amount = 0
    cart_tax_amount = 0
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for pid, item in request.session['cart_data_obj'].items():
            cart_subtotal_amount += int(item['qty']) * float(item['price'])
            cart_tax_amount += (int(item['qty']) * float(item['price'])) * 0.0635
            cart_total_amount += (int(item['qty']) * float(item['price'])) * 1.0635
            item['total_price'] = int(item['qty']) * float(item['price'])

        try:
            order = Order.objects.get(order_id=ORDER_ID)

            order_items = order.order_items.all()
            order_address = order.order_ship_address.all()

            context = {
                    'cart_data': request.session['cart_data_obj'], 
                    'totalcartitems': len(request.session['cart_data_obj']),
                    'cart_subtotal_amount': round(cart_subtotal_amount, 2),
                    'cart_tax_amount': round(cart_tax_amount, 2),
                    'cart_total_amount': round(cart_total_amount, 2),
                    'status': Product.objects.get(pid=item['pid']).product_status,
                    'o': order,
                    'o_items': order_items,
                    'o_address': order_address,
                }
            
            request.session.flush()

            return render(request, 'Core/payment-completed.html', context=context)
        
        except:
            request.session.flush()
            return redirect('Core:index')
    
    else:
        return redirect('Core:index')

@conditional_login_required(login_required)
def payment_failed_view(request):
    return render(request, 'Core/payment-failed.html')


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        host = request.get_host()
        line_items = []
        product_ids =[]
        for pid, item in request.session['cart_data_obj'].items():
            line_items.append(
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(float(item['price']) * 100),
                        'product_data': {
                            'name': item['title']
                        },
                    },
                    'quantity': item['qty'],
                },
            )
            product_ids.append(item['pid'])
        checkout_session = stripe.checkout.Session.create(
            #ui_mode = 'embedded',
            payment_method_types=['card'],
            line_items=line_items,
            metadata={
                'product_ids': ','.join(product_ids)
            },
            mode='payment',
            billing_address_collection='required',
            shipping_address_collection={
              'allowed_countries': ['US', 'CA'],
            },
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 500, "currency": "usd"},
                        "display_name": "Regular Shipping",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 5},
                            "maximum": {"unit": "business_day", "value": 7},
                        },
                    },
                },
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 1500, "currency": "usd"},
                        "display_name": "Next day air",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 1},
                            "maximum": {"unit": "business_day", "value": 1},
                        },
                    },
                },
            ],
            automatic_tax={
                'enabled': True
            },
            success_url=f"http://{host}{reverse(f'Core:payment-completed')}",
            cancel_url=f"http://{host}{reverse('Core:payment-failed')}",
            #return_url=host + '/checkout_now/',
        )
        return redirect(checkout_session.url, code=303)
    

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session_id = event['data']['object']['id']
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['line_items']
        )
        

        customer_email = session['customer_details']['email']

        line_items = session['line_items']['data']
        product_ids = session['metadata']['product_ids'].split(',')


        for index in range(len(line_items)):

            product_id = product_ids[index]
            product = line_items[index]

            
            current_product = Product.objects.get(pid=product_id)
            if int(current_product.quantity) - (product['quantity']) <= 0:
                current_product.quantity = 0
                current_product.product_status = 'sold_out'
            else:
                current_product.quantity = int(current_product.quantity) - (product['quantity'])
            current_product.save()


        a_details = session['shipping_details']['address']
        if a_details['line2'] is not None:
            address = f"{a_details['line1']}, {a_details['line2']}, {a_details['city']}, {a_details['state']}, {a_details['postal_code']}, {a_details['country']}"
        else:
            address = f"{a_details['line1']}, {a_details['city']}, {a_details['state']}, {a_details['postal_code']}, {a_details['country']}"

        order = Order.objects.create(
            order_number="ORDER_NUMBER-" + str(len(Order.objects.all()) + 1),
            order_price=float(session['amount_total'] / 100),
            customer_email=customer_email,
            address=address,
        )

        global ORDER_ID
        ORDER_ID = order.order_id

        shipping_address = ShippingAddress.objects.create(
            order=order,
            address_line_one=session['shipping_details']['address']['line1'],
            address_line_two=session['shipping_details']['address']['line2'],
            address_city=session['shipping_details']['address']['city'],
            address_zip_code=session['shipping_details']['address']['postal_code'],
            address_state=session['shipping_details']['address']['state'],
            address_country=session['shipping_details']['address']['country'],
        )

        billing_address = BillingAddress.objects.create(
            order=order,
            address_line_one=session['customer_details']['address']['line1'],
            address_line_two=session['customer_details']['address']['line2'],
            address_city=session['customer_details']['address']['city'],
            address_zip_code=session['customer_details']['address']['postal_code'],
            address_state=session['customer_details']['address']['state'],
            address_country=session['customer_details']['address']['country'],
        )

        for index in range(len(line_items)):
            product_id = product_ids[index]
            product = line_items[index]
            current_product = Product.objects.get(pid=product_id)
            order_items = OrderItems.objects.create(
                order=order,
                pid=product_id,
                image=current_product.image,
                title=product['description'],
                price=float(product['price']['unit_amount'] / 100),
                quantity=product['quantity'],
                total_price=(float(product['price']['unit_amount'] / 100)) * product['quantity'],
            )

    return HttpResponse(status=200)

@conditional_login_required(login_required)
def order_list_view(request):
    context = {
        'input_text': 'Enter an Order Number'
    }
    return render(request, 'Core/order-list.html', context=context)

@conditional_login_required(login_required)
def order_detail_view(request, oid):
    try:
        order = Order.objects.get(order_id=oid)

        order_items = order.order_items.all()
        order_address = order.order_ship_address.all()

        context = {
            'o': order,
            'o_items': order_items,
            'o_address': order_address,
        }

        return render(request, 'Core/order-detail.html', context=context)
    except ObjectDoesNotExist:

        context = {
            'input_text': 'Order not found. Please enter a valid order number.'
        }
        return render(request, 'Core/order-list.html', context=context)
    

