from django import forms
from .models import Repository, Commit


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

class CommitForm(forms.ModelForm):
    class Meta:
        model = Commit
        fields = ['message','hash']

