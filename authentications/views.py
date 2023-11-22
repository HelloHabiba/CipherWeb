from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.shortcuts import redirect
# Create your views here.
from django.contrib.auth import login, authenticate




class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username", 
        widget=forms.TextInput(
            attrs={
                'class': 'spark-input w-input', 
                'maxlength': '256', 
                'placeholder': 'Enter Your Username', 
                'required': True,
                'id': 'Your-Username---Signup-Form', 
                'name': 'Your-Username---Signup-Form', 
                'data-name': 'Your Username - Signup Form'
            }
        )
    )
    password = forms.CharField(
            label="Password", 
            widget=forms.PasswordInput(
                attrs={
                    'class': 'spark-input w-input', 
                    'maxlength': '256', 
                    'id': 'Password-Sign-up-form', 
                    'name': 'password', 
                    'data-name': 'Password Sign up form', 
                    'required': True
                }
            )
        )

class RegisterForm(forms.Form):
    # Username field
    username = forms.CharField(
        label="Username", 
        widget=forms.TextInput(
            attrs={
                'class': 'spark-input w-input', 
                'maxlength': '256', 
                'placeholder': 'Enter Your Username', 
                'required': True,
                'id': 'Your-Username---Signup-Form', 
                'name': 'Your-Username---Signup-Form', 
                'data-name': 'Your Username - Signup Form'
            }
        ),
    )

    # Password field
    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(
            attrs={
                'class': 'spark-input w-input', 
                'maxlength': '256', 
                'id': 'Password-Sign-up-form', 
                'name': 'password', 
                'data-name': 'Password Sign up form', 
                'required': True
            }
        )
    )

    # Email field
    email = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput(
            attrs={
                'class': 'spark-input w-input', 
                'maxlength': '256', 
                'placeholder': 'Your Email Address', 
                'required': True,
                'id': 'Email-Address-Sign-up-form-2', 
                'name': 'Email-Address-Sign-up-form', 
                'data-name': 'Email Address Sign up form'
            }
        )
    )

class EditForm(forms.Form):
    # Username field
    username = forms.CharField(
        label="Username", 
        widget=forms.TextInput(
            attrs={
                'class': 'spark-input w-input', 
                'maxlength': '256', 
                'placeholder': 'Enter Your Username', 
                'required': False,
                'id': 'Your-Username---Signup-Form', 
                'name': 'Your-Username---Signup-Form', 
                'data-name': 'Your Username - Signup Form',
            }
        ),
        required=False
    )

    # Password field
    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(
            attrs={
                'class': 'spark-input w-input', 
                'maxlength': '256', 
                'id': 'Password-Sign-up-form', 
                'name': 'password', 
                'data-name': 'Password Sign up form', 
                'required': False
            },
        ),
        required=False
    )

    # Email field
    email = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput(
            attrs={
                'class': 'spark-input w-input', 
                'maxlength': '256', 
                'placeholder': 'Your Email Address', 
                'required': False,
                'id': 'Email-Address-Sign-up-form-2', 
                'name': 'Email-Address-Sign-up-form', 
                'data-name': 'Email Address Sign up form'
            }
        ),
        required=False
    )
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = ""
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else :
                error = "Invalid username or password"


    
    return render(request, 'login.html',{'form':LoginForm(), 'error':error})



def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = ""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            from django.contrib.auth.models import User
            user = User.objects.create_user(username=username, email=email, password=password, first_name="first_name", last_name="last_name")
            user.save()
            authenticate(request, username=username,password=password)
            login(request, user)
            return redirect('home')
        else :
            error = "Invalid username or password"
    return render(request, 'register.html',{'form':RegisterForm(), 'error':error})


def logout_page(request):
    logout(request)
    return redirect('/user/login')

def profile_page(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        user = request.user
        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            if username :
                user.username = username
            email = form.cleaned_data.get('email')
            if email:
                user.email = email
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password) 
            user.save()
            authenticate(request, username=username,password=password)
            login(request, user)
    return render(request, 'profile.html', {"form" : EditForm(),"user":request.user})
