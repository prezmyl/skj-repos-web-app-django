
from repos_app import views as repo_views

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# urls project-level

urlpatterns = [
    path('', RedirectView.as_view(url='/repos/', permanent=False)),  # ← root → /repos/ ..localhost cisty se presmeruje at nen 404, kdyz zadam jen ip localhostu be /repo
    path('admin/', admin.site.urls),
    path('repos/', include('repos_app.urls', namespace='repos_app')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', repo_views.signup, name='signup'),


    path('api/repos/', repo_views.api_repos_list, name='api_repos_list'),
    path('api/repos/<int:pk>/', repo_views.api_repo_detail, name='api_repo_detail'),

]
