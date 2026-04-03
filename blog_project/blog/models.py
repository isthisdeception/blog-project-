"""
Blog models - Defines the core data structures for the blog.

Models:
- Category: Blog post categories
- Tag: Blog post tags
- Post: Main blog post model with rich content
- Comment: User comments on posts
- Like: User likes on posts
- Newsletter: Email newsletter subscriptions
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """Blog post category model."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Auto-generate slug from category name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return the URL for posts filtered by this category."""
        return reverse('blog:posts-by-category', kwargs={'slug': self.slug})

    @property
    def post_count(self):
        """Returns the number of published posts in this category."""
        return self.posts.filter(status='published').count()


class Tag(models.Model):
    """Tag for organizing and filtering blog posts."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Auto-generate slug from tag name
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:posts-by-tag', kwargs={'slug': self.slug})


class PostQuerySet(models.QuerySet):
    """Custom queryset manager for Post model.
    
    Provides commonly used filtered querysets as methods."""
    
    def published(self):
        """Return only published posts."""
        return self.filter(status='published')
    
    def recent(self, count=5):
        """Return the most recent published posts."""
        return self.published().order_by('-published_at')[:count]
    
    def popular(self, count=5):
        """Return the most liked published posts."""
        return self.published().annotate(
            like_count=models.Count('likes')
        ).order_by('-like_count', '-published_at')[:count]


class Post(models.Model):
    """Main blog post model with rich content and metadata."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # Featured image displayed on the post card and detail page
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True)
    content = models.TextField(help_text="Write your post content here.")
    
    # Relationships
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Status and dates
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # published_at can be manually set for scheduling
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Custom manager using our QuerySet
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        # Auto-generate slug from title
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure slug uniqueness
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        # Auto-set published_at if not set and status is published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the canonical URL for this post."""
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    @property
    def excerpt(self):
        """Return a short excerpt from the post content (first 200 chars)."""
        if len(self.content) > 200:
            return self.content[:200] + '...'
        return self.content

    @property
    def total_likes(self):
        """Return the total number of likes for this post."""
        return self.likes.count()

    @property
    def total_comments(self):
        """Return the total number of published comments."""
        return self.comments.filter(is_published=True).count()

    def get_related_posts(self, count=3):
        """Return related posts based on shared category or tags."""
        related = Post.objects.published().exclude(pk=self.pk)
        # First, try to find posts with same tags
        if self.tags.exists():
            by_tags = related.filter(tags__in=self.tags.all()).distinct()
            if by_tags.count() >= count:
                return by_tags[:count]
        # Then, posts in the same category
        if self.category:
            by_category = related.filter(category=self.category)
            return by_category[:count]
        # Fallback to recent posts
        return related[:count]


class Comment(models.Model):
    """User comments on blog posts with nested support."""
    
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    content = models.TextField()
    # Parent comment for nested/threaded replies
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_replies(self):
        """Return all direct replies to this comment."""
        return self.replies.filter(is_published=True)


class Like(models.Model):
    """User likes on blog posts (one like per user per post)."""
    
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can only like a post once
        unique_together = ['post', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'


class Newsletter(models.Model):
    """Newsletter subscription model."""
    
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email
