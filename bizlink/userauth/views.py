from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import SignUpForm, LogInForm, EditProfileForm
from .models import BusinessOwner, Customer, Profile, SocialMedia
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
                    first_name=form.cleaned_data['first_name'].title(),
                    last_name=form.cleaned_data['last_name'].title(),
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
            
            user.save()

            # Creating a profile here
            Profile.objects.create(created_by=user)

            return redirect('userauth:user_login')
    
        """ Invalid sign up attempt is handled by
          the built in parameters of each input field and
           by django's secure password criteria """

    else:
        form = SignUpForm()

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

                        return redirect("core:customer_home")
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

@login_required
def edit_profile(request):
    # Get the logged-in user's profile
    profile = get_object_or_404(Profile, created_by=request.user)

    if request.method == 'POST':
        # If the request is POST, process the data
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.mobile = request.POST.get('mobile', profile.mobile)

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            profile.image = request.FILES['profile_image']  # Update the profile image if uploaded

        # Save the changes to the profile
        profile.save()

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Profile updated successfully!'}, status=200)

    # If the request method is not POST, return an error response
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SocialMedia
from django.contrib.auth.decorators import login_required

@login_required
def manage_social_media(request):
    if request.method == 'GET':
        # Fetch existing social media entries
        social_media_entries = SocialMedia.objects.filter(created_by=request.user).values('platform', 'url')
        return JsonResponse(list(social_media_entries), safe=False)

    if request.method == 'POST':
        platform = request.POST.get('platform')
        url = request.POST.get('url')
        action = request.POST.get('action')

        if action == 'save' and platform and url:
            # Save or update the social media entry
            social_media_instance, created = SocialMedia.objects.get_or_create(
                created_by=request.user,
                platform=platform,
                defaults={'url': url}
            )
            if not created:  # If the instance already exists, update the URL
                social_media_instance.url = url
                social_media_instance.save()
            return JsonResponse({'message': 'Social media URL saved successfully!'}, status=200)

        elif action == 'delete' and platform:
            # Delete the social media entry
            SocialMedia.objects.filter(created_by=request.user, platform=platform).delete()
            return JsonResponse({'message': 'Social media URL deleted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request method or missing parameters.'}, status=400)

