from django.shortcuts import render
from django.views import View
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

            order = orders.objects.create(price=price)
            order.items.add(*item_ids)

            context = {
                'items': order_items['items'],
                'price': price
            }
        return render(request, 'customer/order_confirmation.html', context)

