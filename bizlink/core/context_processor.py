from shop.models import Shop, Category, Product, MoreProductImage, CartOrder, CartOrderProduct, ProductReview, Wishlist
from userauth.models import Notification
from django.contrib import messages

############################ Views for Base Template ############################

def base(request):
    user = request.user
    
    # Initialize default values for both authenticated and anonymous users
    categories = []
    wishlist = 0
    notification = 0

    if user.is_authenticated:
        try:
            shopId = request.session.get('current_shop_id')  
            
            if shopId:
                shop = Shop.objects.get(shopId=shopId)
                categories = Category.objects.filter(created_by=shop.created_by)

        except Shop.DoesNotExist:
            messages.warning(request, "An error occurred while accessing shop details.")
        
        try:
            wishlist = Wishlist.objects.filter(created_by=user)

        except Exception as e:  # Catch all exceptions to log the error
            messages.warning(request, "An error occurred while accessing your wishlist.")
            print("Wishlist query error:", str(e))  # Print the error to the console or log it
        
        try:
            notification = Notification.objects.filter(created_by=user)

        except Exception as e:  # Catch all exceptions to log the error
            messages.warning(request, "An error occurred while accessing your notifications.")
            print("Notification query error:", str(e))  # Print the error to the console or log it

    return {
        'categories': categories,
        'wishlist': wishlist,
        'notification': notification,
    }