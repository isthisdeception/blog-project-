"""Blog app URL configuration."""

from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    # Main post list
    path('', views.PostListView.as_view(), name='post-list'),
    
    # Post CRUD
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    
    # Post detail
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    # Author page
    path('author/<str:username>/', views.AuthorPostListView.as_view(), name='posts-by-author'),
    
    # Category and tag filtering
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='posts-by-category'),
    path('tag/<slug:slug>/', views.TagPostListView.as_view(), name='posts-by-tag'),
    
    # Like and comment actions
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/<int:post_pk>/comment/', views.add_comment, name='add-comment'),
]
