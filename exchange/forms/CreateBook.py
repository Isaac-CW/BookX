from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from ..models import Book

class CreateBookForm(forms.ModelForm):
    # This field is required for the lookup but excluded from direct model saving 
    # to force the API call to populate the other required fields.
    
    class Meta:
        model = Book
        fields = ('isbn', 'condition', 'description', "author", "title") # Fields the user inputs directly
        widgets = {
            # Use appropriate styling/placeholders for user experience
            'isbn': forms.TextInput(attrs={'placeholder': 'Enter 10 or 13 digit ISBN'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }