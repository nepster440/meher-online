from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django import forms
from django.contrib.auth import logout

class UserLoginView(LoginView):
    template_name = "login.html"
    
    # Login form ke fields (Username & Password) ko customize karna
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Username field styling aur placeholder
        form.fields['username'].widget = forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'autocomplete': 'off' # Autofill suggestions kam karne ke liye
        })
        
        # Password field styling aur placeholder
        form.fields['password'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
        return form

class UserLogoutView(LogoutView):
    """
    Django 5.0+ aur 6.0 mein LogoutView default roop se POST maangta hai.
    Ye 'get' method allow karega ki user link par click karte hi logout ho jaye.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        # Logout ke baad sidha login page par redirect karega
        return redirect('login')