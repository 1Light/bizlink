from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages

from .forms import SignUpForm, LogInForm
from .models import BusinessOwner, Customer
from shop.models import Shop

# Create your views here.
def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid(): 

            user_type = form.cleaned_data['user_type']

            if user_type == 'business_owner':
                user = BusinessOwner.objects.create_user(
                    email=form.cleaned_data['email'],
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    address=form.cleaned_data['address'],
                    mobile=form.cleaned_data['mobile'],
                    password=form.cleaned_data['password1'],
                    user_type=user_type,
                )

            elif user_type == 'customer':
               
                user = Customer.objects.create_user(
                    email=form.cleaned_data['email'],
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    address=form.cleaned_data['address'],
                    mobile=form.cleaned_data['mobile'],
                    password=form.cleaned_data['password1'],
                    user_type=user_type,
                )
            
            return redirect('userauth:user_login')
    
        """ Invalid sign up attempt is handled by
          the built in parameters of each input field and
           by django's secure password criteria """

    else:
        form = SignUpForm()
        print(form)

    return render(request, "userauth/signup.html", {
        'form': form,
        'title': 'Sign Up'
    })

def user_login(request):

    if request.method == "POST":
        form = LogInForm(data=request.POST)

        if form.is_valid():
            email=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.user_type == user_type:
                    if user.user_type == 'business_owner':
                        login(request, user)
                        
                        # demo line of code for testing
                        return redirect("core:owner_home")

                        if Shop.objects.filter(created_by=user).exists():
                            messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                            # return redirect("core:home") 
                        else:
                            messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                            # return redirect("shop:create_shop")
   
                    elif user.user_type == 'customer':
                        login(request, user)
                        messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                        return redirect("core:customer_home")
                else:
                    messages.error(request, "User type does not match.")
    
    else:
        form = LogInForm()

    return render(request, "userauth/login.html", {
        'form': form,
        'title': 'Log In'
    })

def user_logout(request):
    
    logout(request)
    messages.success(request, "You have been logged out successfully.")

    return redirect("userauth:user_login")