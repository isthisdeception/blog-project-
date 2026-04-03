"""
Blog forms - Forms for creating/editing posts and comments.

Uses Django Crispy Forms for Bootstrap 5 styled forms.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts.
    
    Uses Crispy Forms for beautiful Bootstrap 5 layout."""
    
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'category', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter an engaging title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'Write your amazing content here...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configure Crispy Forms helper for custom layout
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
            Field('title', css_class='form-control form-control-lg'),
            Field('image', css_class='form-control'),
            Field('content', css_class='form-control', rows=12),
            Row(
                Column('category', css_class='col-md-6'),
                Column('tags', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Post', css_class='btn btn-primary btn-lg mt-3'),
        )


class CommentForm(forms.ModelForm):
    """Form for adding comments to blog posts."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('content', css_class='form-control', rows=4),
            Submit('submit', 'Post Comment', css_class='btn btn-outline-primary mt-2'),
        )


class ReplyForm(forms.ModelForm):
    """Form for replying to existing comments."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3,
                'placeholder': 'Write a reply...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('content'),
            Submit('submit', 'Reply', css_class='btn btn-sm btn-primary mt-1'),
        )
