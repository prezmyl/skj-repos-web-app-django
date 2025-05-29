


from repos_app.forms import (CommitForm,
                             RepositoryForm,
                             CommentForm,
                             IssueForm,
                             RepoSearchForm,
                             CommitFilterForm,
                             PullRequestForm)
from repos_app.models import Commit, Repository, Issue, Comment
from .models import Repository, Issue, Comment, PullRequest

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('repos_app:repo_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



# ------------------------------------------
#           CRUD operations for Repository
# ------------------------------------------

# vraci seznam repozitaru, ktere vlastni uzivatel
@login_required
def repo_list(request):
    form = RepoSearchForm(request.GET)
    repos = Repository.objects.filter(owner=request.user)
    if form.is_valid() and form.cleaned_data['query']:
        repos = repos.filter(name__icontains=form.cleaned_data['query'])

    return render(request,
              'repos_app/repo_list.html',
              {
                  'repos': repos,
                  'form': form,
               })

# nacte konkretni repo pokud exists
@login_required
def repo_detail(request, pk):
    repo = get_object_or_404(Repository, pk=pk, owner=request.user)
    return render(request, 'repos_app/repo_detail.html', {'repo': repo})

# GET zobrazi prazdny formular, POST naplni form daty z request
@login_required
def repo_create(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.owner = request.user
            repo.save()
            return redirect( 'repos_app:repo_detail', pk=repo.pk)
    else:
        form = RepositoryForm()

    return render(request, 'repos_app/repo_form.html', {'form': form})


# podbne create, instace=repo -> django vi ze pracujem s jiz existujicim zazname,
@login_required
def repo_update(request, pk):
    repo = get_object_or_404(Repository, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = RepositoryForm(request.POST, instance=repo)
        if form.is_valid():
            form.save()
            return redirect( 'repos_app:repo_detail', pk=repo.pk)
    else:
        form = RepositoryForm(instance=repo)
    return render(request, 'repos_app/repo_form.html', {'form': form, 'repo': repo})



# GET -> ukaze potvrzovaci stranku
# POST -> smaze objekt a presmeruje(redirect) na seznam
@login_required
def repo_delete(request, pk):
    repo = get_object_or_404(Repository,pk=pk, owner=request.user)
    if request.method == 'POST':
        repo.delete()
        return redirect( 'repos_app:repo_list')
    return render(request, 'repos_app/repo_delete.html', {'repo': repo})



# ------------------------------------------
#           CRUD operations for Commit
# ------------------------------------------



def commit_list(request, repo_pk):
    repo = get_object_or_404(Repository, pk=repo_pk, owner=request.user)
    form = CommitFilterForm(request.GET)
    qs = repo.commits.order_by('-timestamp')
    if form.is_valid():
        sd = form.cleaned_data['start_date']
        ed = form.cleaned_data['end_date']
        if sd:
            qs = qs.filter(timestamp__date__gte=sd)
        if ed:
            qs = qs.filter(timestamp__date__lte=ed)
    return render(request, 'repos_app/commit_list.html', {
        'repo': repo,
        'commits': qs,
        'filter_form': form,
    })


@login_required
def commit_create(request, repo_pk):
    repo = get_object_or_404(Repository, pk=repo_pk, owner=request.user)
    if request.method == 'POST':
        form = CommitForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.repository = repo
            commit.author = request.user
            commit.save()
            return redirect('repos_app:commit_detail',
                            repo_pk=repo_pk,
                            hash=commit.hash)
    else:
        form = CommitForm()

    return render(request,
                  'repos_app/commit_form.html',
                  {'form': form, 'repo': repo})

@login_required
def commit_detail(request, repo_pk, hash):
    commit = get_object_or_404(Commit, hash=hash)
    return render(request, 'repos_app/commit_detail.html',
                  {'commit': commit})



# ------------------------------------------
#           CRUD operations for Issues
# ------------------------------------------

@login_required
def issue_list(request, repo_pk):
    repo = get_object_or_404(
        Repository,
        pk=repo_pk,
        owner=request.user
    )
    issues = repo.issues.order_by('-created_at')
    return render(request, 'repos_app/issue_list.html', {
        'repo': repo,
        'issues': issues,
    })


@login_required
def issue_detail(request, repo_pk, pk):
    issue = get_object_or_404(
        Issue,
        pk=pk,
        repository__pk=repo_pk,
        repository__owner=request.user
    )

    # handle comment submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            cm = comment_form.save(commit=False)
            cm.issue = issue
            cm.author = request.user
            cm.save()
            return redirect(
                'repos_app:issue_detail',
                repo_pk=repo_pk,
                pk=pk
            )
    else:
        comment_form = CommentForm()

    # fetch all comments, oldest first
    comments = issue.comments.order_by('created_at')

    return render(request, 'repos_app/issue_detail.html', {
        'repo': issue.repository,
        'issue': issue,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def issue_create(request, repo_pk):
    repo = get_object_or_404(
        Repository,
        pk=repo_pk,
        owner=request.user
    )
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.repository = repo
            issue.author     = request.user
            issue.save()
            form.save_m2m()  # uloží ManyToMany (labels)
            return redirect(
                'repos_app:issue_detail',
                repo_pk=repo.pk,
                pk=issue.pk
            )
    else:
        form = IssueForm()
    return render(request, 'repos_app/issue_form.html', {
        'repo': repo,
        'form': form,
    })

@login_required
def issue_update(request, repo_pk, pk):
    issue = get_object_or_404(
        Issue,
        pk=pk,
        repository__pk=repo_pk,
        repository__owner=request.user
    )
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect(
                'repos_app:issue_detail',
                repo_pk=repo_pk,
                pk=pk
            )
    else:
        form = IssueForm(instance=issue)
    return render(request, 'repos_app/issue_form.html', {
        'repo': issue.repository,
        'form': form,
        'issue': issue,
    })

@login_required
def issue_delete(request, repo_pk, pk):
    issue = get_object_or_404(
        Issue,
        pk=pk,
        repository__pk=repo_pk,
        repository__owner=request.user
    )
    if request.method == 'POST':
        issue.delete()
        return redirect('repos_app:issue_list', repo_pk=repo_pk)
    return render(request, 'repos_app/issue_delete.html', {
        'repo':  issue.repository,
        'issue': issue,
    })

# ------------------------------------------
#           CRUD operations for Pull Request
# ------------------------------------------


@login_required
def pr_list(request, repo_pk):
    repo = get_object_or_404(Repository, pk=repo_pk, owner=request.user)
    prs = repo.pull_requests.order_by('-created_at')
    return render(request, 'repos_app/pr_list.html', {
        'repo': repo,
        'prs':  prs,
    })

@login_required
def pr_create(request, repo_pk):
    repo = get_object_or_404(Repository, pk=repo_pk, owner=request.user)
    if request.method == 'POST':
        form = PullRequestForm(request.POST)
        if form.is_valid():
            pr = form.save(commit=False)
            pr.repository = repo
            pr.author     = request.user
            pr.save()
            form.save_m2m()
            return redirect('repos_app:pr_detail', repo_pk=repo.pk, pk=pr.pk)
    else:
        form = PullRequestForm()
    return render(request, 'repos_app/pr_form.html', {
        'repo': repo,
        'form': form,
    })

@login_required
def pr_detail(request, repo_pk, pk):
    pr = get_object_or_404(
        PullRequest,
        pk=pk,
        repository__pk=repo_pk,
        repository__owner=request.user
    )
    return render(request, 'repos_app/pr_detail.html', {
        'repo': pr.repository,
        'pr':   pr,
    })

@login_required
def pr_merge(request, repo_pk, pk):
    pr = get_object_or_404(
        PullRequest,
        pk=pk,
        repository__pk=repo_pk,
        repository__owner=request.user
    )
    if request.method == 'POST':
        pr.is_merged = True
        pr.save()
    return redirect('repos_app:pr_detail', repo_pk=repo_pk, pk=pk)

@login_required
def pr_update(request, repo_pk, pk):
    pr = get_object_or_404(
        PullRequest,
        pk=pk,
        repository__pk=repo_pk,
        repository__owner=request.user
    )
    if request.method == 'POST':
        form = PullRequestForm(request.POST, instance=pr)
        if form.is_valid():
            form.save()
            return redirect('repos_app:pr_detail', repo_pk=repo_pk, pk=pk)
    else:
        form = PullRequestForm(instance=pr)
    return render(request, 'repos_app/pr_form.html', {
        'repo': pr.repository,
        'form': form,
        'pr':   pr,
    })

@login_required
def pr_delete(request, repo_pk, pk):
    pr = get_object_or_404(
        PullRequest,
        pk=pk,
        repository__pk=repo_pk,
        repository__owner=request.user
    )
    if request.method == 'POST':
        pr.delete()
        return redirect('repos_app:pr_list', repo_pk=repo_pk)
    return render(request, 'repos_app/pr_delete.html', {
        'repo': pr.repository,
        'pr':   pr,
    })




# ------------------------------------------
#           API calls -> machine readable endpoints
# ------------------------------------------

@login_required
def api_repos_list(request):
    """ Return JSON list of all repos owned by the user """
    qs = Repository.objects.filter(owner=request.user)
    data = [
        {
            'id':        r.id,
            'name':      r.name,
            'description': r.description,
            'is_private':  r.is_private,
            'created_at':  r.created_at.isoformat(),
        }
        for r in qs
    ]
    return JsonResponse(data, safe=False)


@login_required
def api_repo_detail(request, pk):
    """ Return JSON detail for one repo by its PK """
    r = get_object_or_404(Repository, pk=pk, owner=request.user)
    data = {
        'id':          r.id,
        'name':        r.name,
        'description': r.description,
        'is_private':  r.is_private,
        'created_at':  r.created_at.isoformat(),
    }
    return JsonResponse(data)


