from shop.models import Shop, Category, Product, MoreProductImage, CartOrder, CartOrderProduct, ProductReview, Wishlist, Address
from django.contrib import messages

############################ Views for Base Template ############################

def base(request):
    user = request.user
    
    if user.is_authenticated:
        categories = Category.objects.filter(created_by=user)
        
        try:
            wishlist = Wishlist.objects.filter(created_by=user)

        except Exception as e:  # Catch all exceptions to log the error
            messages.warning(request, "An error occurred while accessing your wishlist.")
            print("Wishlist query error:", str(e))  # Print the error to the console or log it
            wishlist = 0
    else:
        categories = []  # No categories for anonymous users
        wishlist = 0  # Set wishlist count to 0 for anonymous users

    return {
        'categories': categories,
        'wishlist': wishlist,
    }