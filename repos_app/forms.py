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