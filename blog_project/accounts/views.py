"""
Authentication views - User registration, login, logout, and profile management.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from accounts.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeFormCustom
from blog.models import Post, Newsletter
from pages.models import ContactMessage


def register(request):
    """
    User registration view.
    Creates a new user account and automatically logs them in.
    The Profile is auto-created via the post_save signal.
    """
    if request.user.is_authenticated:
        return redirect('blog:post-list')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 
                f'Welcome, {user.username}! Your account has been created successfully.'
            )
            return redirect('blog:post-list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def custom_login(request):
    """Custom login view with Bootstrap-styled form."""
    if request.user.is_authenticated:
        return redirect('blog:post-list')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'blog:post-list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def custom_logout(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('blog:post-list')


@login_required
def profile(request):
    """View the current user's profile with their posts."""
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    """Edit user profile information including profile picture."""
    if request.method == 'POST':
        # Determine which form was submitted based on presence of fields
        if 'username' in request.POST:
            # Account details form submitted
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
            
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Account details updated successfully!')
                return redirect('accounts:edit-profile')
            # If invalid, re-render with errors (p_form stays unbound)
        elif 'bio' in request.POST or 'profile_picture' in request.FILES or 'profile_picture-clear' in request.POST:
            # Profile form submitted
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=request.user.profile
            )
            
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Profile information updated successfully!')
                return redirect('accounts:edit-profile')
            # If invalid, re-render with errors (u_form stays unbound)
        else:
            # Fallback: initialize both forms fresh
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form,
    })


@login_required
def change_password(request):
    """Allow user to change their password."""
    if request.method == 'POST':
        form = PasswordChangeFormCustom(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeFormCustom(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})


@user_passes_test(lambda u: u.is_staff, login_url='blog:post-list')
def admin_dashboard(request):
    """Custom admin dashboard for site overview."""
    total_posts = Post.objects.count()
    total_users = get_user_model().objects.count()
    total_messages = ContactMessage.objects.count()
    new_messages_count = ContactMessage.objects.filter(status='new').count()
    total_subscribers = Newsletter.objects.filter(is_active=True).count()
    recent_messages = ContactMessage.objects.all()[:10]
    recent_posts = Post.objects.order_by('-created_at')[:5]

    context = {
        'total_posts': total_posts,
        'total_users': total_users,
        'total_messages': total_messages,
        'new_messages_count': new_messages_count,
        'total_subscribers': total_subscribers,
        'recent_messages': recent_messages,
        'recent_posts': recent_posts,
    }
    return render(request, 'accounts/dashboard.html', context)
