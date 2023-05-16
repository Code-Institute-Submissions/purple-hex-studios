from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_services(request):
    """ A view to show all services, including sorting and search queries """

    services = Product.objects.all()

    context = {
        'services': services,
    }

    return render(request, 'services/services.html', context)


def service_detail(request, product_id):
    """ A view to show individual product details """

    service = get_object_or_404(Product, pk=product_id)

    context = {
        'service': service,
    }

    return render(request, 'services/service_detail.html', context)