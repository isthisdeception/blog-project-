"""
Blog admin - Customized Django admin for blog models.

Features:
- Rich admin display with images, counts, status badges
- Filterable and searchable post list
- Inline comments for posts
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from blog.models import Category, Tag, Post, Comment, Like, Newsletter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for blog categories."""
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for blog tags."""
    list_display = ['name', 'slug', 'post_count_display']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def post_count_display(self, obj):
        """Show number of posts with this tag."""
        return obj.posts.count()
    post_count_display.short_description = 'Posts'


class CommentInline(admin.TabularInline):
    """Inline display of comments within a post admin page."""
    model = Comment
    extra = 0
    fields = ['author', 'content', 'created_at', 'is_published']
    readonly_fields = ['author', 'content', 'created_at']
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin for blog posts with rich display and filtering."""
    
    list_display = [
        'title_display', 
        'author', 
        'category', 
        'status_badge', 
        'published_at', 
        'comments_count',
    ]
    list_filter = [
        'status', 
        'category', 
        'tags', 
        'created_at', 
        'published_at',
    ]
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    inlines = [CommentInline]
    list_per_page = 25
    
    fieldsets = (
        ('Post Details', {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('Organization', {
            'fields': ('category', 'tags')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def title_display(self, obj):
        """Truncate long titles for the list view."""
        if len(obj.title) > 50:
            return obj.title[:50] + '...'
        return obj.title
    title_display.short_description = 'Title'

    def status_badge(self, obj):
        """Display status with a colored badge."""
        if obj.status == 'published':
            return format_html(
                '<span style="color: #198754; font-weight: bold;">Published</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">Draft</span>'
        )
    status_badge.short_description = 'Status'

    def comments_count(self, obj):
        """Show number of comments on this post."""
        count = obj.comments.filter(is_published=True).count()
        return count
    comments_count.short_description = 'Comments'

    def get_queryset(self, request):
        """Optimize query with prefetch for comments count."""
        return super().get_queryset(request).prefetch_related('comments')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin for managing blog comments."""
    list_display = ['author_display', 'post_display', 'created_at', 'is_published']
    list_filter = ['is_published', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    list_editable = ['is_published']
    date_hierarchy = 'created_at'

    def author_display(self, obj):
        return obj.author.username
    author_display.short_description = 'Author'

    def post_display(self, obj):
        if len(obj.post.title) > 40:
            return obj.post.title[:40] + '...'
        return obj.post.title
    post_display.short_description = 'Post'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin for newsletter subscriptions."""
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
