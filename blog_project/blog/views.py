"""
Blog views - Class-based and function-based views for the blog app.

Contains views for:
- Post listing with pagination, search, filtering
- Post detail with comments and likes
- Post CRUD (create, update, delete)
- Author page
- Category and tag filtering
- Comment management
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from blog.models import Post, Comment, Like, Category, Tag
from blog.forms import PostForm, CommentForm, ReplyForm


class PostListView(ListView):
    """
    Main blog post listing page.
    Displays published posts in a paginated card grid.
    Supports search via query parameter.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6  # 6 posts per page
    ordering = ['-published_at']

    def get_queryset(self):
        """Filter queryset to only published posts and apply search."""
        queryset = Post.objects.published()
        
        # Search by title or content
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass search query to template for form value
        context['query'] = self.request.GET.get('q', '')
        return context


class PostDetailView(DetailView):
    """
    Single post detail page.
    Shows full post content, comments, like button, and related posts.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        """Show published posts, or any post to its author."""
        queryset = Post.objects.all()
        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        return queryset.filter(status='published')

    def post(self, request, *args, **kwargs):
        """Handle comment submission on the post detail page."""
        self.object = self.get_object()
        
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect(self.object.get_absolute_url())
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment. Please try again.')
        
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # Get top-level comments (not replies)
        context['comments'] = post.comments.filter(
            is_published=True, 
            parent__isnull=True
        ).prefetch_related('replies').order_by('-created_at')
        
        # Comment form
        context['comment_form'] = CommentForm()
        
        # Reply forms for each comment
        context['reply_forms'] = {
            comment.id: ReplyForm()
            for comment in context['comments']
        }
        
        # Check if user has liked this post
        if self.request.user.is_authenticated:
            context['user_has_liked'] = post.likes.filter(
                user=self.request.user
            ).exists()
        else:
            context['user_has_liked'] = False
        
        # Related posts section
        context['related_posts'] = post.get_related_posts()
        
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post. Requires login."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    
    def form_valid(self, form):
        """Set the author to the current logged-in user."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing blog post. Only the author can edit."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """Only the post author can edit."""
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog post. Only the author can delete."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        """Only the post author can delete."""
        post = self.get_object()
        return self.request.user == post.author


class AuthorPostListView(ListView):
    """
    Display all published posts by a specific author.
    Shows author info alongside the post list.
    """
    template_name = 'blog/author_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        """Return published posts by this specific author."""
        self.author_username = self.kwargs.get('username')
        return Post.objects.published().filter(
            author__username=self.author_username
        ).select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        context['author'] = get_object_or_404(
            User, 
            username=self.kwargs.get('username')
        )
        return context


class CategoryPostListView(ListView):
    """Display all published posts in a specific category."""
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.published().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostListView(ListView):
    """Display all published posts with a specific tag."""
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.published().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


@login_required
def like_post(request, pk):
    """
    AJAX view for toggling likes on a post.
    Creates or removes a Like object based on current state.
    """
    post = get_object_or_404(Post, pk=pk)
    
    like, created = Like.objects.get_or_create(
        post=post, 
        user=request.user
    )
    
    if not created:
        # User already liked - remove the like
        like.delete()
        liked = False
    else:
        liked = True
    
    # Return JSON response for AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes
        })
    
    # Fallback redirect for non-AJAX requests
    messages.success(
        request, 
        'Post liked!' if liked else 'Like removed.'
    )
    return redirect(post.get_absolute_url())


@login_required
def add_comment(request, post_pk):
    """Handle comment submission on a blog post."""
    post = get_object_or_404(Post, pk=post_pk, status='published')
    
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # If replying to an existing comment, set parent
            if parent_id:
                parent_comment = get_object_or_404(
                    Comment, 
                    pk=parent_id, 
                    post=post
                )
                comment.parent = parent_comment
            
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, 'Error adding comment. Please try again.')
    
    return redirect(post.get_absolute_url())
