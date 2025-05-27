
from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path, include
from repos_app import views as repo_views

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/repos/', permanent=False)),  # ← root → /repos/ ..localhost cisty se presmeruje at nen 404, kdyz zadam jen ip localhostu be /repo
    path('admin/', admin.site.urls),
    path('repos/', include('repos_app.urls', namespace='repos_app')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', repo_views.signup, name='signup'),

]
