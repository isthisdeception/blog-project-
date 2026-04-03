"""
Context processor for sidebar data available across all templates.

Returns recent posts, popular posts, categories, and tags
to include in the sidebar on every page.
"""

from blog.models import Post, Category, Tag


def sidebar_context(request):
    """Provides common sidebar data to all templates."""
    return {
        'sidebar_recent_posts': Post.objects.recent(5),
        'sidebar_popular_posts': Post.objects.popular(5),
        'sidebar_categories': Category.objects.all(),
        'sidebar_tags': Tag.objects.all(),
    }
