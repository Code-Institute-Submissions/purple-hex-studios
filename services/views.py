from django.shortcuts import render
from .models import Product

# Create your views here.

def all_services(request):
    """ A view to show all services, including sorting and search queries """

    services = Product.objects.all()

    context = {
        'services': services,
    }

    return render(request, 'services/services.html', context)