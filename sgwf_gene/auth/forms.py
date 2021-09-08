from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _U
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Senha'
        self.fields['username'].label = 'Usuário ou E-mail'

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'id_username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'id_password'}))


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'id_email'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Senha antiga'
        self.fields['new_password1'].label = 'Nova senha'
        self.fields['new_password2'].label = 'Confirmar nova senha'

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'id_old_password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'id_new_password_1'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'id_new_password_2'}))


class CreateUserForm(forms.Form):
    username = forms.CharField(label='Nome de Usuário', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[RegexValidator(regex=r'^[A-Za-z\d_]+$', message='Seu usuário deve conter apenas letras, números ou _.')])
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}), validators=[validate_password])
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nome', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if len(cleaned_data.get('username')) < 4:
            raise ValidationError(_U('Seu nome de usuário deve ter pelo menos 4 caracteres.'))

        if User.objects.filter(username=username).count() > 0:
            raise ValidationError(_U('Este usuário já existe.'))

        return username

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            raise ValidationError(_U('Este email já está associado a um usuário.'))

        return email

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')

        if pass1 is not None and pass1 != pass2:
            self.add_error('password2', 'As senhas não correspondem.')
