from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
import urllib.parse

from .models import (
    Product,
    SolarRequest,
    Appliance,
    SolarOnlyRequest,
    Article,
    Comment,
    Project
)

from .forms import OrderForm
from django.core.paginator import Paginator

def index(request):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-id')

    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 3)  # 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/index.html', {
        'page_obj': page_obj
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})
# add to cart----------------------------------------------------------



def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart

    return redirect('shop')
#cart view-------------------------------------------------------
def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, quantity in cart.items():
        product = Product.objects.get(id=id)
        product.quantity = quantity
        product.total_price = product.price * quantity
        total += product.total_price
        products.append(product)

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })

from django.core.paginator import Paginator

def shop(request):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-id')

    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 9)  # 9 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/shop.html', {
        'page_obj': page_obj
    })


def checkout(request):
    cart = request.session.get('cart', {})
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            # ---------- MESSAGE ----------
            message = f"""
New Order from NELSMART

Customer Name: {name}
Email: {email}
Phone: {phone}

Items:
"""

            total = 0

            for id, quantity in cart.items():
                product = Product.objects.get(id=int(id))
                message += f"- {product.name} x{quantity} = {product.price * quantity} FCFA\n"
                total += product.price * quantity

            message += f"\nTotal Amount: {total} FCFA"

            # ---------- SEND EMAIL ----------
            # try:
            #     email_msg = EmailMessage(
            #         'New Order Received',
            #         message,
            #         from_email='Nelsonatud@yahoo.com',
            #         to=['Nelsonatud@yahoo.com'],
            #     )
            #     email_msg.send()
            # except Exception as e:
            #     print("Email error:", e)

            # ---------- WHATSAPP ----------
            encoded_message = urllib.parse.quote(message)

            # Your WhatsApp number
            whatsapp_number = "237675940002"

            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

            # clear cart
            request.session['cart'] = {}

            # redirect to WhatsApp
            return redirect(whatsapp_url)

    return render(request, 'store/checkout.html', {'form': form})



def free_site_visit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        message = request.POST.get('message')
        other = request.POST.get('other_service')

        # ✅ multiple services
        services = request.POST.getlist('services')
        services_text = ", ".join(services)

        if other:
            services_text += f", Other: {other}"

        # ---------- EMAIL MESSAGE ----------
        email_message = f"""
NEW FREE SITE VISIT REQUEST

Name: {name}
Phone: {phone}
Address: {location}

Services Needed:
{services_text}

Message:
{message}
"""

        try:
            email = EmailMessage(
                subject='New Free Site Visit Request',
                body=email_message,
                from_email='Nelsonatud@yahoo.com',   # you can keep this for now
                to=['Nelsonatud@yahoo.com'],       # your email
            )
            email.send()
        except Exception as e:
            pass

        # ---------- WHATSAPP ----------
        whatsapp_text = urllib.parse.quote(email_message)
        whatsapp_number = "237675940002"

        return redirect(f"https://wa.me/{whatsapp_number}?text={whatsapp_text}")

    return render(request, 'store/free_visit.html')




def get_informed(request):
    articles = Article.objects.all()
    return render(request, 'store/get_informed.html', {'articles': articles})


def info_detail(request, slug):
    article = Article.objects.get(slug=slug)
    comments = Comment.objects.filter(article=article)

    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')

        Comment.objects.create(
            article=article,
            name=name,
            message=message
        )

    return render(request, f'store/info/{slug}.html', {
        'article': article,
        'comments': comments
    })


def like_article(request, slug):
    article = Article.objects.get(slug=slug)
    article.likes += 1
    article.save()
    return JsonResponse({'likes': article.likes})

from .models import SolarRequest, Appliance
from django.shortcuts import render
from django.core.mail import EmailMessage
import urllib.parse

def solar_cost(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        message = request.POST.get('message')

        appliances = request.POST.getlist('appliance[]')
        quantities = request.POST.getlist('quantity[]')
        hours_list = request.POST.getlist('hours[]')
        day_hours_list = request.POST.getlist('day_hours[]')

        total = 0

        # CREATE MAIN REQUEST
        solar_request = SolarRequest.objects.create(
            email=email,
            phone=phone,
            state=state,
            message=message
        )

        # LOOP MULTIPLE APPLIANCES
        for i in range(len(appliances)):

            # skip empty rows
            if not quantities[i] or not hours_list[i]:
                continue

            try:
                qty = int(quantities[i])
                hrs = int(hours_list[i])
            except ValueError:
                continue

            cost = qty * hrs * 50
            total += cost

            Appliance.objects.create(
                solar_request=solar_request,  # ✅ fixed
                name=appliances[i],
                quantity=qty,
                hours=hrs,
                day_hours=int(day_hours_list[i] or 0)
            )

        # EMAIL
        full_message = f"""
New Solar Request

Email: {email}
Phone: {phone}
State: {state}

Total Cost: {total} FCFA
"""

        try:
            EmailMessage(
                'Solar Cost Request',
                full_message,
                to=['Nelsonatud@yahoo.com']
            ).send()
        except:
            pass

        # AUTO WHATSAPP REDIRECT
        whatsapp_text = urllib.parse.quote(full_message)
        whatsapp_url = f"https://wa.me/237675940002?text={whatsapp_text}"

        return render(request, 'store/solar_redirect.html', {
            'whatsapp_url': whatsapp_url
        })

    return render(request, 'store/solar_cost.html')

#----solar only cost


def solar_only_cost(request):
    if request.method == 'POST':

        data = SolarOnlyRequest.objects.create(
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            state=request.POST.get('state'),
            battery_capacity=request.POST.get('battery_capacity'),
            battery_qty=request.POST.get('battery_qty'),
            inverter_power=request.POST.get('inverter_power'),
            voltage=request.POST.get('voltage'),
            message=request.POST.get('message'),
        )

        whatsapp_message = f"""
Solar Only Request:
Email: {data.email}
Phone: {data.phone}
Location: {data.state}

Battery: {data.battery_capacity} x {data.battery_qty}
Inverter: {data.inverter_power}
Voltage: {data.voltage}
        """

        # AUTO WHATSAPP REDIRECT
        whatsapp_text = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/237675940002?text={whatsapp_text}"

        return render(request, 'store/solar_redirect.html', {
            'whatsapp_url': whatsapp_url
        })

    return render(request, 'store/solar_only_cost.html')

def street_light(request):
    return render(request, 'store/info/street-light.html')

def solar_farm(request):
    return render(request, 'store/info/solar_farm.html')

def lithium_battery(request):
    return render(request, 'store/info/lithium_battery.html')

def solar_system(request):
    return render(request, 'store/info/solar_system.html')
from .models import Project

def projects(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'store/projects.html', {'projects': projects})

def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'store/project_detail.html', {'project': project})
def return_policy(request):
    return render(request, 'store/return_policy.html')
def privacy_policy(request):
    return render(request, 'store/privacy_policy.html')
def payment_delivery(request):
    return render(request, 'store/payment_delivery.html')
def terms(request):
    return render(request, 'store/terms.html')
def about(request):
    return render(request, 'store/about.html')
def culture(request):
    return render(request, 'store/culture.html')
def basic_plan(request):
    return render(request, 'store/basic_plan.html')
def standard_plan(request):
    return render(request, 'store/standard_plan.html')
def premium_plan(request):
    return render(request, 'store/premium_plan.html')
