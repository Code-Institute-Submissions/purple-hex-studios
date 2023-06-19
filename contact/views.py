from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import ContactForm


def contact(request):

    """
    a view displaying contact form
    and contact form submission
    """

    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent')
            return redirect(reverse("contact"))

        else:
            messages.warning(request, 'Message failed')

    template = 'contact/contact.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
