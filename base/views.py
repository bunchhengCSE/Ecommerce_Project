from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category, Order, OrderProduct
from django.db.models import Q
import json
from django.http import JsonResponse

# Create your views here.


def home_page(request):
    some_products = Product.objects.all()[0:6]
    context = {'some_products': some_products}
    return render(request, 'base/home.html', context)


def shop_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.all()
    if q == '':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            Q(category__name__icontains=q)|Q(name__icontains=q))
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_product = paginator.get_page(page_number)
    context = {'page_product': page_product, 'categories': categories}
    return render(request, 'base/shop.html', context)

def about_page(request):
    return render(request,'base/about.html')

def contact_page(request):
    return render(request,'base/contact.html')
def cart_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderproduct_set.all()
        cartItems = order.get_cart_items
        context = {'cartItems': cartItems, 'order': order, 'items': items}
    return render(request, 'base/cart.html', context)


def update_product(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer)

    orderItem, created = OrderProduct.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        product.in_stock = (product.in_stock-1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        product.in_stock = (product.in_stock+1)
    elif action == 'remove_all':
        product.in_stock = (product.in_stock+orderItem.quantity)
        orderItem.quantity = 0
    orderItem.save()
    product.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)



def detail_product(request,pk):
    product=Product.objects.get(id=pk)
    product_the_some_categories = Product.objects.filter(Q(category__name__icontains=product.category)).exclude(Q(
            name__icontains=product.name))
    context = {'product':product,'product_the_some_categories':product_the_some_categories}
    return render(request, 'base/detail_product.html',context)