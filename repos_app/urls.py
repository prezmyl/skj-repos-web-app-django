from django.urls import path

from repos_app import views

app_name = 'repos_app'
urlpatterns = [
    path('',           views.repo_list,    name='repo_list'),
    path('new/',       views.repo_create,  name='repo_create'),
    path('<int:pk>/',  views.repo_detail,  name='repo_detail'),
    path('<int:pk>/edit/',   views.repo_update,  name='repo_update'),
    path('<int:pk>/delete/', views.repo_delete,  name='repo_delete'),
]
