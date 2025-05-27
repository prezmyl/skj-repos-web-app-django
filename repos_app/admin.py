from django.contrib import admin
from .models import Repository, Commit, Label, Issue, Comment, PullRequest

admin.site.register(Repository)
admin.site.register(Commit)
admin.site.register(Label)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(PullRequest)
