from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import ContactForm


def contact(request):

    """
    a view displaying contact form
    and contact form submission
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Message sent')
            return HttpResponseRedirect('/contact?submitted=True')

        else:
            form = ContactForm()
            messages.warning(request, 'Message failed')

    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            form = ContactForm()

    form = ContactForm()
    template = 'contact/contact.html'
    context = {
        'form': form,
    }

    return render(request, template, context)