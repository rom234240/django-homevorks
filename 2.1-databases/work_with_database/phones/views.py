from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone

def index(request):
    return redirect('catalog')

def show_catalog(request):
    template = 'catalog.html'
    
    sort_param = request.GET.get('sort', 'name')
    
    if sort_param == 'name':
        phones = Phone.objects.all().order_by('name')
    elif sort_param == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif sort_param == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all()
    
    return render(request, template, {'phones': phones})

def show_product(request, slug):
    template = 'product.html'
    phone = get_object_or_404(Phone, slug=slug)
    return render(request, template, {'phone': phone})