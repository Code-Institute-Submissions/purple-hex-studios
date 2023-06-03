from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

from .forms import ProductForm

# Create your views here.

def all_services(request):
    """ A view to show all services, including sorting and search queries """

    services = Product.objects.all()
    query = None
    categories = None

    if request.GET:

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            services = services.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('services'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            services = services.filter(queries)

    context = {
        'services': services,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'services/services.html', context)


def service_detail(request, product_id):
    """ A view to show individual product details """

    service = get_object_or_404(Product, pk=product_id)

    context = {
        'service': service,
    }

    return render(request, 'services/service_detail.html', context)

def add_service(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            messages.success(request, 'Successfully added service')
            return redirect(reverse('service_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add service. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'services/add_service.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

def edit_service(request, product_id):
    """ Edit a service in the store """
    service = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated service')
            return redirect(reverse('service_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update service. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=service)
        messages.info(request, f'You are editing {product.name}')

    template = 'services/edit_service.html'
    context = {
        'form': form,
        'service': service,
    }

    return render(request, template, context)

def delete_service(request, product_id):
    """ Delete a product from the store """
    service = get_object_or_404(Product, pk=product_id)
    service.delete()
    messages.success(request, 'Service deleted')
    return redirect(reverse('services'))