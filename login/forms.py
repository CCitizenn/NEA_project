from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form): #the form for logging into an existing account
    username = forms.CharField(
        max_length=16, 
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

class RegisterForm(forms.ModelForm): #form for creating an account
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self): #check to see if the two p match before registering an account
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email