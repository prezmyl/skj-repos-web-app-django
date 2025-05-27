from django import forms
from .models import Repository


# --------------------------------------
#           FORMs definitions
# --------------------------------------

class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'description', 'is_private']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }