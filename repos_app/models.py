# repos/models.py
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# kazda trioda predstavuju jednu tabulku v db

class Repository(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'name')

    def __str__(self):
        return f'{self.owner.username}/{self.name}'


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='commits')
    author     = models.ForeignKey(User,       on_delete=models.CASCADE, related_name='commits')
    message    = models.CharField(max_length=255)
    hash       = models.CharField(max_length=40, unique=True)
    timestamp  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.hash[:7]} – {self.message}'


class Label(models.Model):
    name  = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#cccccc')

    def __str__(self):
        return self.name


class Issue(models.Model):
    repository  = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='issues')
    author      = models.ForeignKey(User,       on_delete=models.CASCADE, related_name='issues')
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_open     = models.BooleanField(default=True)
    labels      = models.ManyToManyField(Label, blank=True, related_name='issues')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Issue #{self.id}: {self.title}'


class Comment(models.Model):
    author     = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='comments')
    issue      = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on Issue #{self.issue.id}'


class PullRequest(models.Model):
    repository    = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='pull_requests')
    author        = models.ForeignKey(User,       on_delete=models.CASCADE, related_name='pull_requests')
    title         = models.CharField(max_length=200)
    description   = models.TextField(blank=True)
    source_branch = models.CharField(max_length=100)
    target_branch = models.CharField(max_length=100)
    is_merged     = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = 'merged' if self.is_merged else 'open'
        return f'PR #{self.id} {self.title} [{status}]'
