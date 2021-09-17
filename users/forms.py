from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.validators import UnicodeUsernameValidator
from . models import Keyword
username_validator = UnicodeUsernameValidator()

class UserRegisterForm(UserCreationForm):
    
    full_name = forms.CharField(label=('Name'), max_length=100, min_length=4, required=True, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
    email = forms.EmailField(max_length=50, help_text='Required a valid email address.',
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                )
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        help_text=_('Required 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
   

    class Meta:
        model = User
        fields = ('full_name','email',  'username', 'password1', 'password2', )


class KeywordForm(forms.ModelForm):
    
    keyword = forms.CharField(label='Search', max_length=100)
    
    
    class Meta:
        model = Keyword
        fields = ('keyword',)        