from django import forms
from .models import Presentation

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['title', 'description', 'file', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }