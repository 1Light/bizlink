from shop.models import Shop, Category, Product, MoreProductImage, CartOrder, CartOrderProduct, ProductReview, Wishlist
from userauth.models import Notification
from django.contrib import messages
from chat.models import GroupMessage
from django.db.models import OuterRef, Exists
from chat.models import ReadReceipt, ChatGroup

############################ Views for Base Template ############################

def base(request):
    user = request.user
    print(user)
    
    # Initialize default values for both authenticated and anonymous users
    categories = []
    wishlist = 0
    notification = 0
    inbox_count = 0
    shop = None
    total_unread_messages = 0  # Initialize unread messages count to 0
    
    if user.is_authenticated:
        if user.user_type == "customer":
            try:
                shopId = request.session.get('current_shop_id')
                
                if shopId:
                    shop = Shop.objects.get(shopId=shopId)
                    categories = Category.objects.filter(created_by=shop.created_by)

            except Shop.DoesNotExist:
                messages.warning(request, "An error occurred while accessing shop details.")
        
        elif user.user_type == "business_owner":
            categories = Category.objects.filter(created_by=user)
            shop = Shop.objects.get(created_by=user)
        
        # Fetch wishlist and notifications for the authenticated user
        try:
            wishlist = Wishlist.objects.filter(created_by=user)
        except Exception as e:
            messages.warning(request, "An error occurred while accessing your wishlist.")
            print("Wishlist query error:", str(e))
        
        try:
            notification = Notification.objects.filter(created_by=user)
        except Exception as e:
            messages.warning(request, "An error occurred while accessing your notifications.")
            print("Notification query error:", str(e))

        # Calculate total unread messages for the user
        chat_groups = ChatGroup.objects.filter(members=user)
        for chat_group in chat_groups:
            # Get all messages in the group where the current user is NOT the author
            chat_messages = GroupMessage.objects.filter(group=chat_group).exclude(author=user)
            
            # Filter messages that have not been read by the current user
            unread_messages = chat_messages.filter(
                ~Exists(ReadReceipt.objects.filter(message=OuterRef('pk'), user=user))
            )
            total_unread_messages += unread_messages.count()

    return {
        'user': user,
        'shop': shop,
        'categories': categories,
        'wishlist': wishlist,
        'notification': notification,
        'total_unread_messages': total_unread_messages,  # Add unread messages to context
    }
