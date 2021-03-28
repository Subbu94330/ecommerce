from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, "get_cart_items": 0, 'shipping':False}
        cartitems = order['get_cart_items']

    products = Product.objects.all()
    context = {"products": products, 'cartitems': cartitems}
    return render(request, "stores/store.html", context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, "get_cart_items": 0}
        cartitems = order['get_cart_items']
    context = {"items": items, "order":order, 'cartitems': cartitems, 'shipping':False}
    return render(request, "stores/cart.html", context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, "get_cart_items": 0, 'shipping':False}
        cartitems = order['get_cart_items']
    context = {"items": items, "order":order, 'cartitems': cartitems}
    return render(request, "stores/checkout.html", context)

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('id:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1 ) 
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1 )
    orderitem.save()

    if orderitem.quantity <= int(0):
        orderitem.delete()
    return JsonResponse("data added", safe =False)


def proceesorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['formm']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete= True
        order.save()

        if order.shipping == True:
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zip_code = data['shipping']['zip_code']





    return JsonResponse("payment submitted...", safe=False)