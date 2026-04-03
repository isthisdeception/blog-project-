"""Authentication and profile forms with Crispy Forms integration."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from accounts.models import Profile


class UserRegisterForm(UserCreationForm):
    """Registration form with styled fields using Crispy Forms."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email...'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-control form-control-lg'),
            Field('email', css_class='form-control form-control-lg'),
            Field('password1', css_class='form-control form-control-lg'),
            Field('password2', css_class='form-control form-control-lg'),
            Submit('submit', 'Create Account', css_class='btn btn-primary btn-lg w-100 mt-3'),
        )


class UserUpdateForm(forms.ModelForm):
    """Form for updating basic user information."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Submit('submit', 'Update Profile', css_class='btn btn-primary mt-3'),
        )


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating extended profile information."""
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'website', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Field('profile_picture', css_class='form-control'),
            Field('bio', css_class='form-control'),
            Row(
                Column('location', css_class='col-md-6'),
                Column('website', css_class='col-md-6'),
            ),
            Submit('submit', 'Save Changes', css_class='btn btn-primary mt-3'),
        )


class PasswordChangeFormCustom(PasswordChangeForm):
    """Styled password change form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('old_password', css_class='form-control form-control-lg'),
            Field('new_password1', css_class='form-control form-control-lg'),
            Field('new_password2', css_class='form-control form-control-lg'),
            Submit('submit', 'Change Password', css_class='btn btn-warning btn-lg mt-3'),
        )
