from django.shortcuts import render, get_list_or_404
from .models import Example


def examples(request):
    """
    Get examples.
    """
    examples = get_list_or_404(Example)

    context = {
         'examples': examples,
    }

    return render(request, 'examples/examples.html', context)
