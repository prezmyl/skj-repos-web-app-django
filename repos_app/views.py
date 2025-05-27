from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from repos_app.forms import RepositoryForm
from repos_app.models import Repository


# repos_app/views.py
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

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


# --------------------------------------
#           CRUD operations
# --------------------------------------

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
            return redirect( 'repos_app/repo_detail', pk=repo.pk)
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
            return redirect( 'repos_app/repo_detail', pk=repo.pk)
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
        return redirect( 'repos_app/repo_list')
    return render(request, 'repos_app/repo_delete.html', {'repo': repo})


