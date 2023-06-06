from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Contact form
    """
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message',)

    def __init__(self, *args, **kwargs):
        """
        Placeholder text
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'email': 'Email Address',
            'message': 'Message',
        }