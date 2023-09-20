from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


from .models import Account
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
 

# @never_cache
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)

            return redirect('/')
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect('login')

    return render(request, "accounts/login.html")

def register_user(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            role = form.cleaned_data['role']  # Get the role from the form

            # Create the user with the specified role
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
                phone_number=phone_number,
                role=role  # Assign the role to the user
            )

            # email verification
            current_site = get_current_site(request)

            messages.success(request, "Successfully registered!")
            return redirect('manage_user')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/add-user.html', context)


@login_required
def profile(request):
    user = request.user
    username = user.username
    email = user.email
    full_name = user.full_name
    phone_number = user.phone_number
    role = user.role

    context = {
        'user': user,
        'username': username,
        'email': email,
        'full_name':full_name,
        'phone_number':phone_number,
        'role':role,

    }

    return render(request, 'pages/profile.html', context)

login_required(login_url='/login')
@never_cache
def logout_view(request):
    logout(request)
    return redirect('login')