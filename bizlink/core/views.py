from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import timedelta
import json
from django.contrib import messages
from django.db.models import Q
from taggit.models import Tag
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.utils.dateparse import parse_datetime

from shop.forms import EditShop, CreateFeature
from userauth.forms import SocialMediaForm

from shop.models import Shop, Category, Product, DiscountedProduct, MoreProductImage, CartOrder, CartOrderProduct, ProductReview, Wishlist, Feature, FeaturedProduct, NewArrival
from userauth.models import Profile, SocialMedia, Notification

############################ Views for Business Owners ############################
############################ Views for Business Owners ############################
############################ Views for Business Owners ############################

@never_cache
def owner_home(request):
    user = request.user
    categories = Category.objects.filter(created_by=user)
    products = Product.objects.filter(created_by=user).order_by("-created_at")

    wishlist_items = Wishlist.objects.filter(created_by=user).values_list('product__productId', flat=True)

    return render(request, "core/owner/home.html", {
        'products': products,
        'categories': categories,
        'wishlist_items': wishlist_items,
    })

def product(request):
    user = request.user

    if user.user_type == 'business_owner':  
    # Owner: Fetch the shop based on the logged-in user
        products = Product.objects.filter(created_by=user).order_by("-created_at")

        if not products.exists():  # Check if the queryset is empty
            messages.error(request, "You don't have any products yet.")

    elif user.user_type == 'customer':
        # Customer: Use session-stored shopId to view a shop
        shopId = request.session.get('current_shop_id')
        if shopId:
            shop = get_object_or_404(Shop, shopId=shopId)
            products = Product.objects.filter(shop=shop).order_by("-created_at")
        else:
            messages.error(request, "No products available.")

    return render(request, "core/owner/product.html", {
        'products': products,
    })

def product_detail(request, productId):
    user = request.user

    if user.user_type == 'business_owner':  
    # Owner: Fetch the shop based on the logged-in user
        try:
            product = Product.objects.get(created_by=user, productId=productId)
            shop = Shop.objects.get(created_by=user)
        except Product.DoesNotExist:
            messages.error(request, "No product detail available.")

    elif user.user_type == 'customer':
        # Customer: Use session-stored shopId to view a shop
        shopId = request.session.get('current_shop_id')
        if shopId:
            shop = get_object_or_404(Shop, shopId=shopId)
            product = Product.objects.get(shop=shop, productId=productId)
        else:
            messages.error(request, "No products available.")
    
    product_images = product.more_product_images.all()
    product_videos = product.more_product_videos.all()
    related_products = Product.objects.filter(category=product.category).exclude(productId=productId)
    
    try:
        discounted_product = DiscountedProduct.objects.get(product=product)
    except DiscountedProduct.DoesNotExist:
        discounted_product = None

    return render(request, "core/owner/product-detail.html", {
        'user': user,
        'product': product,
        'product_images': product_images,
        'product_videos': product_videos,
        'shop': shop,
        'related_products': related_products,
        'discounted_product': discounted_product,
    })

def apply_discount(request, productId):
    if request.method == 'POST':
        try:
            # Parse the request data
            data = json.loads(request.body.decode('utf-8'))
            new_price = data.get('new_price')
            discount_until = data.get('discount_until')

            # Validate that new price and discount_until are provided
            if not new_price or not discount_until:
                return JsonResponse({'success': False, 'message': 'New price and discount time are required.'})

            # Convert new_price to a float
            new_price = float(new_price)

            # Parse discount_until into a datetime object
            discount_until = parse_datetime(discount_until)

            # Check if discount_until is valid
            if discount_until is None or discount_until <= datetime.now():
                return JsonResponse({'success': False, 'message': 'Discount time must be in the future.'})

            # Find the product
            product = get_object_or_404(Product, productId=productId)

            # Validate that the new price is lower than the original price
            if new_price >= product.price:
                return JsonResponse({'success': False, 'message': 'New price must be lower than the original price.'})

            # Get the shop from the product
            shop = product.shop

            # Create or update the discounted product
            discounted_product, created = DiscountedProduct.objects.update_or_create(
                product=product,
                defaults={
                    'new_price': new_price,
                    'discount_until': discount_until,
                    'shop': shop,  # Ensure the shop is passed
                    'created_by': request.user,
                }
            )

            return JsonResponse({'success': True, 'message': 'Discount applied successfully!'})

        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid input data. Please provide valid numbers and dates.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def delete_discount(request, productId):
    # Get the user from the request
    user = request.user
    product = Product.objects.get(productId=productId)

    if request.method == 'DELETE':
        print("Attempting to delete discount for productId:", productId)  # Debugging line
        try:
            # Find the discounted product
            discounted_product = get_object_or_404(DiscountedProduct, product__productId=productId)
            
            # Check for the has_discount_ended parameter
            has_discount_ended = request.GET.get('has_discount_ended', 'false').lower() == 'true'

            # If the countdown has ended, create a notification
            if has_discount_ended:

                Notification.objects.create(created_by=user, message=f'The discount has ended for the product: {product.name}')

            # Delete the discounted product
            discounted_product.delete()

            return JsonResponse({'success': True, 'message': 'Discount deleted successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def category(request):
    user = request.user
    
    if user.user_type == 'business_owner':  
        categories = Category.objects.filter(created_by=user).order_by("-created_at")

        if not categories.exists():  # Check if the queryset is empty
            messages.error(request, "You don't have any categories yet.")

    elif user.user_type == 'customer':
        # Customer: Use session-stored shopId to view a shop
        shopId = request.session.get('current_shop_id')
        if shopId:
            shop = get_object_or_404(Shop, shopId=shopId)
            categories = Category.objects.filter(shop=shop).order_by("-created_at")
        else:
            messages.error(request, "No categories available.")

    return render(request, "core/owner/category.html", {
        'categories': categories,
    })

def category_detail(request, categoryId):
    user = request.user

    if user.user_type == 'business_owner':  
        try:
            category = Category.objects.get(created_by=user, categoryId=categoryId)
            shop = Shop.objects.get(created_by=user)
        except Category.DoesNotExist:
            messages.error(request, "No category detail available.")

    elif user.user_type == 'customer':
        # Customer: Use session-stored shopId to view a shop
        shopId = request.session.get('current_shop_id')
        if shopId:
            shop = get_object_or_404(Shop, shopId=shopId)
            category = Category.objects.get(shop=shop, categoryId=categoryId)
        else:
            messages.error(request, "No products available.")
    
    products = Product.objects.filter(shop=shop, category=category)

    return render(request, "core/owner/category-detail.html", {
        'category': category,
        'products': products,
    })

def tag(request, tag_slug=None):
    products = Product.objects.all().order_by("-created_at")

    tag = None
    if tag_slug:
        products = products.filter(tags__slug=tag_slug)
        tag = get_object_or_404(Tag, slug=tag_slug)

    return render(request, "core/owner/tag.html", {
        "products": products,
        "tag": tag,
    })

def search(request):
    query = request.GET.get('q', '')
    user = request.user

    # Initial search based on query
    products = Product.objects.filter(created_by=user).select_related('shop').order_by("-created_at")

    # Handle cases where query is invalid or trivial
    if query.strip() in ['.', '', '*']:
        products = products.none()

    # Handle invalid or trivial queries
    else:
        if query:

            keywords = [keyword.strip() for keyword in query.split(',') if keyword.strip()]
            query_filter = Q()

            for keyword in keywords:
                query_filter |= Q(name__icontains=keyword) | Q(description__icontains=keyword)

            products = products.filter(query_filter)
    
    request.session['searched_products'] = list(products.values_list('productId', flat=True))
    
    return render(request, "core/owner/search.html", {
        'products': products,
        'query': query,
    })

def filter_searched_product(request):
    categories = request.GET.getlist("category[]")
    shops = request.GET.getlist("shop[]")
    
    # Get min and max price from the request
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # Get the searched product IDs from the session
    searched_product_ids = request.session.get('searched_products', [])
    
    # Use productId for filtering
    products = Product.objects.filter(productId__in=searched_product_ids).distinct()

    if len(categories) > 0:
        products = products.filter(category__categoryId__in=categories).distinct()

    if len(shops) > 0:
        products = products.filter(shop__shopId__in=shops).distinct()

    # Filter by price range if provided
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    data = render_to_string("core/owner/filtered-product.html", {
        'products': products,
    })

    return JsonResponse({
        "data": data,
    })

@login_required
def wishlist(request):
    user = request.user

    if request.method == "POST":
        product_id = request.POST.get("id")
        # Get the wishlist item and delete it
        wishlist_item = get_object_or_404(Wishlist, id=product_id, created_by=user)
        wishlist_item.delete()
        
        # Optionally, return the updated wishlist count
        wishlist_count = Wishlist.objects.filter(created_by=user).count()
        
        return JsonResponse({"success": True, "wishlist_count": wishlist_count})

    # Handle GET request
    wishlist_products = Wishlist.objects.filter(created_by=user)

    return render(request, "core/owner/wishlist.html", {
        'wishlist_products': wishlist_products,
    })

@login_required
def notification(request):
    user = request.user

    if request.method == "POST":
        notificationId = request.POST.get("id")
        # Get the wishlist item and delete it
        notification = get_object_or_404(Notification, notificationId=notificationId, created_by=user)
        notification.delete()
        
        # Optionally, return the updated notification count
        notification_count = Notification.objects.filter(created_by=user).count()
        
        return JsonResponse({"success": True, "notification_count": notification_count})

    # Handle GET request
    notifications = Notification.objects.filter(created_by=user).order_by('-created_at')

    return render(request, "core/owner/wishlist.html", {
        'notifications': notifications,
    })

@login_required
def owner_account(request):
    user = request.user
    profile = Profile.objects.get(created_by=user)
    notifications = Notification.objects.filter(created_by=user).order_by('-created_at')

    return render(request, "core/owner/owner-account.html", {
        'user': user,
        'profile': profile,
        'notifications': notifications,
    })

@login_required  # Ensure the user is authenticated
def add_to_wishlist(request):
    product_id = request.GET.get('id')
    print(f"Product ID: {product_id}")  # Debug line
    product = Product.objects.get(productId=product_id)
    user = request.user

    context = {}

    # Check if the product is already in the user's wishlist
    wishlist_item = Wishlist.objects.filter(product=product, created_by=user).first()

    if wishlist_item:
        # If it exists, remove it
        wishlist_item.delete()
        context = {
            "removed": True,  # Indicate the product was removed
        }
    else:
        # If it doesn't exist, add it to the wishlist
        Wishlist.objects.create(product=product, created_by=user)
        context = {
            "added": True,  # Indicate the product was added
        }

    # Calculate the current wishlist count for the user
    wishlist_count = Wishlist.objects.filter(created_by=user).count()
    context["wishlist_count"] = wishlist_count  # Add the count to the response

    return JsonResponse(context)

@login_required
def wishlist(request):
    user = request.user

    if request.method == "POST":
        product_id = request.POST.get("id")
        # Get the wishlist item and delete it
        wishlist_item = get_object_or_404(Wishlist, id=product_id, created_by=user)
        wishlist_item.delete()
        
        # Optionally, return the updated wishlist count
        wishlist_count = Wishlist.objects.filter(created_by=user).count()
        
        return JsonResponse({"success": True, "wishlist_count": wishlist_count})

    # Handle GET request
    wishlist_products = Wishlist.objects.filter(created_by=user)

    return render(request, "core/owner/wishlist.html", {
        'wishlist_products': wishlist_products,
    })


def admin(request):
    user = request.user
    products = Product.objects.filter(created_by=user)
    shop = Shop.objects.get(created_by=user)
    features = Feature.objects.filter(created_by=user, shop=shop)
    create_feature_form = CreateFeature()
    featured_products = FeaturedProduct.objects.filter(created_by=user)
    new_arrivals = NewArrival.objects.filter(created_by=user)
    social_media_form = SocialMediaForm()

    return render(request, "core/owner/admin.html", {
        'shop': shop,
        'features': features,
        'products': products,
        'create_feature_form': create_feature_form,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'social_media_form': social_media_form,
    })

############################ Views for Shop ############################
@never_cache
def owner_shop(request):
    user = request.user
    shop = None

    if user.user_type == 'business_owner':  
    # Owner: Fetch the shop based on the logged-in user
        try:
            shop = Shop.objects.get(created_by=user)
        except Shop.DoesNotExist:
            messages.error(request, "You don't have a shop registered.")

    elif user.user_type == 'customer':
        # Customer: Use session-stored shopId to view a shop
        shopId = request.session.get('current_shop_id')
        if shopId:
            shop = get_object_or_404(Shop, shopId=shopId)
        else:
            messages.error(request, "No products available.")

    social_media = SocialMedia.objects.filter(created_by=shop.created_by)
    features = Feature.objects.filter(created_by=shop.created_by)
    featured_products = FeaturedProduct.objects.filter(created_by=shop.created_by)
    new_arrivals = NewArrival.objects.filter(created_by=shop.created_by)
    discounted_products = DiscountedProduct.objects.filter(created_by=shop.created_by, shop=shop)
    wishlist_items = Wishlist.objects.filter(created_by=user).values_list('product__productId', flat=True)

    return render(request, "core/owner/shop.html", {
        'shop': shop,
        'social_media': social_media,
        'features': features,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'discounted_products': discounted_products,
        'wishlist_items': wishlist_items,
    })

############################ Views for Admin ############################

def update_shop(request):
    user = request.user
    shop = Shop.objects.get(created_by=user)  

    if request.method == 'POST':
        form = EditShop(request.POST, request.FILES, instance=shop)

        if form.is_valid():
            form.save()

            return redirect("core:owner_shop") 
        
        else: 
            print(form.errors)

    else:
        form = EditShop(instance=shop)

    return render(request, 'core/owner/admin.html', {
        'form': form,
        'shop': shop
    })

def create_feature(request):

    user = request.user
    shop = Shop.objects.get(created_by=user)
    features = Feature.objects.filter(created_by=user)

    if request.method == "POST":
        form = CreateFeature(request.POST, request.FILES)
    
        if form.is_valid():

            if features.count() > 10:
                # Limit reached, return an error or a message
                messages.error("Feature limit reached")
                return redirect("core:home")
        
        feature = form.save(commit=False)
        feature.shop = shop
        feature.created_by = request.user
        feature.save()
        
    else:
        form = CreateFeature()
    
    return render(request, "core/owner/shop.html", {
        'shop': shop,
        'features': features,
        'form': form
})

def add_featured_product(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])
            
            # Validate input
            if not product_ids:
                return JsonResponse({'success': False, 'message': 'No products selected.'})

            # Assuming you have a way to get the current shop and user
            shop = get_object_or_404(Shop, created_by=request.user) 
            user = request.user

            # Create FeaturedProduct instances
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                # Check if the item is already featured
                if not FeaturedProduct.objects.filter(shop=shop, product=product).exists():
                    FeaturedProduct.objects.create(shop=shop, created_by=user, product=product)
            
            return JsonResponse({'success': True})

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'One or more products do not exist.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
def delete_featured_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])

            if not product_ids:
                return JsonResponse({'success': False, 'message': 'No products selected.'})

            # Get the shop owned by the current user
            shop = get_object_or_404(Shop, created_by=request.user)

            # Delete the FeaturedProduct instances
            FeaturedProduct.objects.filter(shop=shop, product_id__in=product_ids).delete()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
def add_new_arrival(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])
            
            # Validate input
            if not product_ids:
                return JsonResponse({'success': False, 'message': 'No items selected.'})

            # Assuming you have a way to get the current shop and user
            shop = get_object_or_404(Shop, created_by=request.user) 
            user = request.user

            # Create NewArrival instances
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                # Check if the item is already added to new arrival
                if not NewArrival.objects.filter(shop=shop, product=product).exists():
                    NewArrival.objects.create(shop=shop, created_by=user, product=product)
            
            return JsonResponse({'success': True})

        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'One or more products do not exist.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def delete_new_arrival(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])

            if not product_ids:
                return JsonResponse({'success': False, 'message': 'No products selected.'})

            # Get the shop owned by the current user
            shop = get_object_or_404(Shop, created_by=request.user)

            # Delete the FeaturedProduct instances
            NewArrival.objects.filter(shop=shop, product_id__in=product_ids).delete()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

############################ Views for Customers ############################
############################ Views for Customers ############################
############################ Views for Customers ############################

@never_cache
def customer_home(request):

    return render(request, "core/customer/home.html")

@never_cache
def shop(request):

    shops = Shop.objects.all().order_by("name")

    return render(request, "core/customer/shop.html", {
        'shops': shops
    }) 

@never_cache
def visit_shop(request, shopId):
    user = request.user
    request.session['current_shop_id'] = shopId
    
    shop = Shop.objects.get(shopId=shopId)

    # Fetch the same data as before
    social_media = SocialMedia.objects.filter(created_by=shop.created_by)
    features = Feature.objects.filter(created_by=shop.created_by)
    featured_products = FeaturedProduct.objects.filter(shop=shop)
    new_arrivals = NewArrival.objects.filter(shop=shop)
    discounted_products = DiscountedProduct.objects.filter(shop=shop)
    wishlist_items = Wishlist.objects.filter(created_by=user).values_list('product__productId', flat=True)

    return render(request, "core/owner/shop.html", {
        'shop': shop,
        'social_media': social_media,
        'features': features,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'discounted_products': discounted_products,
        'wishlist_items': wishlist_items,
    })