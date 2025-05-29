from django.urls import path

from repos_app import views

# urls app-level

app_name = 'repos_app'
urlpatterns = [
    # repa
    path('',
         views.repo_list,
         name='repo_list'),
    path('new/',
         views.repo_create,
         name='repo_create'),
    path('<int:pk>/',
         views.repo_detail,
         name='repo_detail'),
    path('<int:pk>/edit/',
         views.repo_update,
         name='repo_update'),
    path('<int:pk>/delete/',
         views.repo_delete,
         name='repo_delete'),

    #commits
    path('<int:repo_pk>/commits/',
         views.commit_list,
         name='commit_list'),
    path('<int:repo_pk>/commits/new/',
         views.commit_create,
         name='commit_create'),
    path('<int:repo_pk>/commits/<str:hash>/',
         views.commit_detail,
         name='commit_detail'),

    #Issues
    path(
        '<int:repo_pk>/issues/',
        views.issue_list,
        name='issue_list'
    ),
    path(
        '<int:repo_pk>/issues/new/',
        views.issue_create,
        name='issue_create'
    ),
    path(
        '<int:repo_pk>/issues/<int:pk>/',
        views.issue_detail,
        name='issue_detail'
    ),
    path(
        '<int:repo_pk>/issues/<int:pk>/edit/',
        views.issue_update,
        name='issue_update'
    ),
    path(
        '<int:repo_pk>/issues/<int:pk>/delete/',
        views.issue_delete,
        name='issue_delete'
    ),


]
