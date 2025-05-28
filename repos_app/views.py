from repos_app.forms import RepositoryForm
from repos_app.models import Repository

from repos_app.forms import CommitForm
from repos_app.models import Commit

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Repository
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
    repos = Repository.objects.filter(owner=request.user)
    return render(request, 'repos_app/repo_list.html', {'repos': repos})

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

@login_required
def commit_list(request, repo_pk):
    repo = get_object_or_404(Repository, pk=repo_pk, owner=request.user)
    return render(request,'repos_app/commit_list.html',{'repo':repo,'commits':repo.commits.all()})


@login_required
def commit_create(request, repo_pk):
    repo = get_object_or_404(Repository, pk=repo_pk, owner=request.user)
    if request.method == 'POST':
        form = CommitForm(request.POST)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.repo = repo
            commit.save()
            return redirect('repos_app:commit_detail', repo_pk=repo_pk, hash=commit.hash)
    else:
        form = CommitForm()

    return render(request, 'repos_app/commit_detail.html', {'form': form, 'repo': repo})

@login_required
def commit_detail(request, repo_pk, hash):
    commit = get_object_or_404(Commit, hash=hash)
    return render(request, 'repos_app/commit_detail.html', {'commit': commit})





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
