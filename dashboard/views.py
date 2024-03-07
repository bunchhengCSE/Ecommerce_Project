from django.shortcuts import render,redirect
from base.models import Product,Category
from .forms import ProductForm
from django.db.models import Q
# Create your views here.

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.all()
    if q == '':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            Q(category__name__icontains=q)|Q(name__icontains=q))
    context = {'products': products, 'categories': categories}
    return render(request,'dashboard/index.html',context)


def insert_product(request):
    form = ProductForm()
    categories = Category.objects.all()
    if request.method == "POST":
        category_name = request.POST.get('category')
        category,created = Category.objects.get_or_create(name=category_name)
        Product.objects.create(
            name=request.POST.get('name'),
            category = category,
            price = request.POST.get('price'),
            in_stock = request.POST.get('in_stock'),
            thumbnail = request.FILES['thumbnail'],
            description = request.POST.get('description'),
        )
        return redirect('dashboard:index')
    context = {'form':form,'categories':categories}
    return render(request,'dashboard/product_form.html',context)


def update_product(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    categories = Category.objects.all()
    if request.method == "POST":
        category_name = request.POST.get('category')
        category,created = Category.objects.get_or_create(name=category_name)
        product.name = request.POST.get('name')
        product.category = category
        product.in_stock = request.POST.get('in_stock')
        product.thumbnail = request.FILES['thumbnail']
        product.description = request.POST.get('description')
        
        product.save()
       
        return redirect('dashboard:index')
    context = {'form':form,'categories':categories,'product':product}
    return render(request,'dashboard/product_form.html',context)


def remove_product(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:index')
    return render(request,'dashboard/remove_product.html',{'obj': product})
    