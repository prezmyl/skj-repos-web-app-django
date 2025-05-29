from django import forms
from .models import Repository, Commit, Issue, Label, Comment


# --------------------------------------
#           FORMs definitions -> validace a vykresleni
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


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'is_open', 'labels']
        widgets = {
            'labels': forms.CheckboxSelectMultiple,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }


class RepoSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='Search Repositories',
        widget=forms.TextInput(attrs={
            'placeholder': 'repo name...',
            'class': 'form-control',})
    )


class CommitFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        label='From',
        widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'})
    )
    end_date = forms.DateField(
        required=False,
        label='To',
        widget=forms.DateInput(attrs={'type':'date', 'class':'form-control'})
    )

