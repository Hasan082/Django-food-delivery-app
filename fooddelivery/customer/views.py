from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem as Menu, OrderModel as orders, Category


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        entre = Menu.objects.filter(category__name__contains='Entre')
        snacks = Menu.objects.filter(category__name__contains='Snacks')
        desserts = Menu.objects.filter(category__name__contains='Desserts')
        drinks = Menu.objects.filter(category__name__contains='Drinks')
        apptizer = Menu.objects.filter(category__name__contains='Appetizers')
        context = {
            'entre': entre,
            'snacks': snacks,
            'desserts': desserts,
            'drinks': drinks,
            'apptizer': apptizer
        }
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = Menu.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            order_items['items'].append(item_data)
            price = 0
            item_ids = []

            for item in order_items['items']:
                price += item["price"]
                item_ids.append(item["id"])

            order = orders.objects.create(
                price=price,
                name=name,
                email=email,
                street=street,
                city=city,
                state=state,
                zip_code=zip_code
            )
            order.items.add(*item_ids)

            body = ('Thank you for your order from Foodie! Your food is being made and will be delivered to you soon!\n'
                    f'Your total is ${price}\n'
                    'Thank you again for your order!')
            
            subject = 'Thanks for your order'
            message = body
            sender_email = 'dr.has82@example.com'
            recipient_list = [email]

            # Send email function
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False)

            context = {
                'items': order_items['items'],
                'price': price
            }
        return render(request, 'customer/order_confirmation.html', context)

