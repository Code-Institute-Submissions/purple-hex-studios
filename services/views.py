from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Service, Category

from .forms import ServiceForm

# Create your views here.


def all_services(request):
    """ A view to show all services, including sorting and search queries """

    services = Service.objects.all()
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
                messages.error(request,
                               "You didn't enter any search criteria!"
                               )
                return redirect(reverse('services'))

            queries = Q(name__icontains=query) | Q(description__icontains=query),  # noqa
            services = services.filter(queries)

    context = {
        'services': services,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'services/services.html', context)


def service_detail(request, service_id):
    """ A view to show individual Service details """

    service = get_object_or_404(Service, pk=service_id)

    context = {
        'service': service,
    }

    return render(request, 'services/service_detail.html', context)


@login_required
def add_service(request):
    """ Add a Service to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('services'))

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            messages.success(request, 'Successfully added service')
            return redirect(reverse('service_detail', args=[service.id]))
        else:
            messages.error(request,
                           'Failed to add service. Please ensure the form is valid.',  # noqa
                           )
    else:
        form = ServiceForm()

    template = 'services/add_service.html'
    context = {
        'form': form,

    }

    return render(request, template, context)


@login_required
def delete_service(request, service_id):
    """ Delete a Service from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('services'))

    service = get_object_or_404(Service, pk=service_id)
    service.delete()
    messages.success(request, 'Service deleted')
    return redirect(reverse('services'))


@login_required
def edit_service(request, service_id):
    """ Edit a service in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('service_detail'))

    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated service')
            return redirect(reverse('service_detail', args=[service_id]))
        else:
            messages.error(request, 'Failed to update service. Please ensure the form is valid.'),  # noqa
    else:
        form = ServiceForm(instance=service)
        messages.info(request, f'You are editing {service.name}')

    template = 'services/edit_service.html'
    context = {
        'form': form,
        'service': service,
    }

    return render(request, template, context)
