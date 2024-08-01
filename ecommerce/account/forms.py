from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django import forms

from django.forms.widgets import PasswordInput, TextInput


# Registration form

class CreateUserForm(UserCreationForm):

    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super(CreateUserForm,self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    # Email validation
    def clean_email(self):
        email=self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use!')

        if len(email) >= 350:
            raise forms.ValidationError('Your email is too long!')

        return email

# Login form

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget = TextInput())
    password = forms.CharField(widget = PasswordInput())

# Update form

class UpdateUserForm(forms.ModelForm):

    class Meta:
        
        model = User
        fields = ['username', 'email']
        exclude = ['password1','password1']


    def __init__(self,*args,**kwargs):
        super(UpdateUserForm,self).__init__(*args, **kwargs)

        self.fields['email'].required = True
    
    password = None
    
    # Email validation
    def clean_email(self):
        email=self.cleaned_data.get("email")
        
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use!')

        if len(email) >= 350:
            raise forms.ValidationError('Your email is too long!')

        return email