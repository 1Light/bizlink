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

from shop.forms import EditShop, CreateFeature, EditProductForm, MoreProductImageForm, MoreProductVideoForm, EditCategoryForm, CreateCategoryForm, CreateProductForm
from userauth.forms import SocialMediaForm

from shop.models import Shop, Category, Product, DiscountedProduct, MoreProductImage, MoreProductVideo, CartOrder, CartOrderProduct, ProductReview, Wishlist, Feature, FeaturedProduct, NewArrival, TransactionLog, ProductVideo
from userauth.models import Profile, SocialMedia, Notification

######################################################################################
###################################### Customer ######################################
######################################################################################

""" Home """

@never_cache
def customer_home(request):

    return render(request, "core/customer/home.html")

""" Shop """

def shop_collection(request):

    shops = Shop.objects.all().order_by("name")

    return render(request, "core/customer/shop.html", {
        'shops': shops
    })

def search_customer(request):
    query = request.GET.get('q', '')

    # Initial search based on query
    shops = Shop.objects.all().order_by("-created_at")

    # Handle cases where query is invalid or trivial
    if query.strip() in ['.', '', '*']:
        shops = shops.none()

    # Handle invalid or trivial queries
    else:
        if query:

            keywords = [keyword.strip() for keyword in query.split(',') if keyword.strip()]
            query_filter = Q()

            for keyword in keywords:
                query_filter |= Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(address__icontains=keyword)

            shops = shops.filter(query_filter)
    
    request.session['searched_shops'] = list(shops.values_list('shopId', flat=True))
    
    return render(request, "core/customer/shop.html", {
        'shops': shops,
        'query': query,
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

######################################################################################
####################################### Owner ########################################
######################################################################################

""" Search """

def search_owner(request):
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

""" Shop """

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
    categories = Category.objects.filter(created_by=shop.created_by)
    features = Feature.objects.filter(created_by=shop.created_by)
    featured_products = FeaturedProduct.objects.filter(created_by=shop.created_by)
    new_arrivals = NewArrival.objects.filter(created_by=shop.created_by)
    discounted_products = DiscountedProduct.objects.filter(created_by=shop.created_by, shop=shop)
    wishlist_items = Wishlist.objects.filter(created_by=user).values_list('product__productId', flat=True)

    return render(request, "core/owner/shop.html", {
        'user': user,
        'shop': shop,
        'social_media': social_media,
        'features': features,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'discounted_products': discounted_products,
        'categories': categories,
        'wishlist_items': wishlist_items,
    })

""" Admin """

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
    shop = get_object_or_404(Shop, created_by=user)
    features = Feature.objects.filter(created_by=user)

    if request.method == "POST":
        form = CreateFeature(request.POST, request.FILES)

        if form.is_valid():
            # Check if the feature limit is reached
            if features.count() >= 5:  # Changed to >= to enforce the limit
                messages.error(request, "Feature limit reached. You can only create up to 6 features.")
                return redirect("core:admin")

            feature = form.save(commit=False)
            feature.shop = shop
            feature.created_by = request.user
            feature.save()
            messages.success(request, "Feature created successfully!")
            return redirect("core:admin")  # Redirect after successful creation

    else:
        form = CreateFeature()

    return render(request, "core/owner/shop.html", {
        'shop': shop,
        'features': features,
        'form': form
    })

def delete_feature(request):
    try:
        # Load the JSON data from the request body
        data = json.loads(request.body)
        feature_ids = data.get('feature_ids', [])  # Get the list of feature IDs

        if not feature_ids:
            return JsonResponse({'success': False, 'message': 'No features selected.'})

        # Get the shop owned by the current user
        shop = get_object_or_404(Shop, created_by=request.user)

        # Delete the Featured instances associated with the shop
        Feature.objects.filter(shop=shop, featureId__in=feature_ids).delete()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def add_featured_product(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])

            # Validate input
            if not product_ids:
                return JsonResponse({'success': False, 'message': 'No products selected.'})

            # Get the current shop and user
            shop = get_object_or_404(Shop, created_by=request.user)
            user = request.user

            # Check how many featured products already exist for the shop
            existing_featured_count = FeaturedProduct.objects.filter(shop=shop).count()
            print(existing_featured_count)

            # Calculate how many products can still be featured
            remaining_slots = 12 - existing_featured_count  
            print(remaining_slots)

            # Convert product_ids to integers for proper comparison
            product_ids = [int(pid) for pid in product_ids]

            # Find products that are already featured
            already_featured = FeaturedProduct.objects.filter(shop=shop, product__id__in=product_ids).values_list('product__id', flat=True)
            print(already_featured)

            # Filter out the already featured products from the selected products
            products_to_add = [pid for pid in product_ids if pid not in already_featured]
            print(products_to_add)

            # Check if the number of products to add exceeds the available slots
            if len(products_to_add) > remaining_slots:
                if existing_featured_count == 12:
                    return JsonResponse({'success': False, 'message': 'A maximum of 12 featured products is allowed.'})
                else:
                    return JsonResponse({'success': False, 'message': f'Only {remaining_slots} more products can be featured.'})

            # Check if all selected products are already featured
            elif len(products_to_add) == 0:
                return JsonResponse({'success': False, 'message': 'All selected items have already been featured.'})

            # Create FeaturedProduct instances for the new products
            for product_id in products_to_add:
                product = Product.objects.get(id=product_id)
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

            # Check how many new arrival products already exist for the shop
            existing_new_arrival_count = NewArrival.objects.filter(shop=shop).count()
            print(existing_new_arrival_count)

            # Calculate how many products can still be featured
            remaining_slots = 12 - existing_new_arrival_count
            print(remaining_slots)

            # Convert product_ids to integers for proper comparison
            product_ids = [int(pid) for pid in product_ids]

            # Find products that are already marked as new arrivals
            already_new_arrivals = NewArrival.objects.filter(shop=shop, product__id__in=product_ids).values_list('product__id', flat=True)
            print(already_new_arrivals)

            # Filter out the already new arrival products from the selected products
            new_products_to_add = [pid for pid in product_ids if pid not in already_new_arrivals]
            print(new_products_to_add)

            # Only check if new products exceed the available slots, not the already existing ones
            if len(new_products_to_add) > remaining_slots:

                if (existing_new_arrival_count == 12):
                    return JsonResponse({'success': False, 'message': 'A maximum of 12 new arrivals is allowed.'})
                
                else: 
                    return JsonResponse({'success': False, 'message': f'Only {remaining_slots} more products can be placed as new arrivals.'})
            
            elif len(new_products_to_add) == 0:
                return JsonResponse({'success': False, 'message': 'All selected items have already been added to the new arrival section'})
            
            # Create NewArrival instances for the new products
            for product_id in new_products_to_add:
                product = Product.objects.get(id=product_id)
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


""" Category """

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

""" Product """

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
    
    wishlist_items = Wishlist.objects.filter(created_by=user).values_list('product__productId', flat=True)

    return render(request, "core/owner/product.html", {
        'products': products,
        'wishlist_items': wishlist_items,
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
    print(product_videos)
    related_products = Product.objects.filter(category=product.category).exclude(productId=productId)[:4]
    
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
            
            # Check how many discounts already exist across all products
            existing_discounts_count = DiscountedProduct.objects.count()

            if existing_discounts_count >= 13: 
                return JsonResponse({'success': False, 'message': 'A maximum of 12 discounts can be applied across all products.'})

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

""" Factory """

def factory(request):
    # Initialize forms
    category_form = CreateCategoryForm()
    product_form = CreateProductForm()
    more_product_image_form = MoreProductImageForm()  # Initialize the form for more product images
    more_product_video_form = MoreProductVideoForm()  # Initialize the form for more product videos
    
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        
        # Handling category form submission
        if 'category_form_submit' in request.POST:
            category_form = CreateCategoryForm(request.POST, request.FILES)
            if category_form.is_valid():
                category = category_form.save(commit=False)
                category.created_by = request.user
                category.shop = request.user.user_shop
                category.save()

        # Handling product form submission
        elif 'product_form_submit' in request.POST:
            product_form = CreateProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.shop = request.user.user_shop
                product.created_by = request.user  

                # Save the product first
                product.save()

                # Handle main video upload
                if 'video' in request.FILES:  
                    video_description = product_form.cleaned_data.get('video-description', "")
                    product_video = ProductVideo(
                        created_by=request.user,
                        video=request.FILES['video'],
                        description=video_description
                    )
                    product_video.save()
                    product.video = product_video  # Link the Product to the ProductVideo instance

                # Handling more product images
                # Collect all uploaded images
                for index in range(1, len(request.FILES) + 1):
                    image_key = f'image{index}'  # Assuming fields are named as 'image1', 'image2', etc.
                    if image_key in request.FILES:
                        image = request.FILES[image_key]
                        more_product_image = MoreProductImage(
                            product=product,
                            image=image
                        )
                        more_product_image.save()

                # Handling more product videos
                # Collect all uploaded videos and their descriptions
                for index in range(1, len(request.FILES) + 1):
                    video_key = f'video{index}'
                    if video_key in request.FILES:
                        video = request.FILES[video_key]
                        description_key = f'video-description-{index}'
                        video_description = request.POST.get(description_key, "")
                        
                        more_product_video = MoreProductVideo(
                            product=product,
                            video=video,
                            description=video_description
                        )
                        more_product_video.save()

    return render(request, "core/owner/factory.html", {
        'category_form': category_form,
        'product_form': product_form,
        'more_product_image_form': more_product_image_form,  
        'more_product_video_form': more_product_video_form,
    })

""" Inventory """

def inventory_context(user):

    products = Product.objects.filter(created_by=user).order_by("name")
    categories = Category.objects.filter(created_by=user).order_by("name")
    edit_product_form = EditProductForm()
    edit_category_form = EditCategoryForm()
    more_product_image_form = MoreProductImageForm()
    more_product_video_form = MoreProductVideoForm()

    return {
        'products': products,
        'edit_product_form': edit_product_form,
        'edit_category_form': edit_category_form,
        'categories': categories,
        'more_product_image_form': more_product_image_form,
        'more_product_video_form': more_product_video_form,
    }

def inventory(request):
    user = request.user
    context = inventory_context(user)

    return render(request, "core/owner/inventory.html", context)

def category_inventory_view(request, categoryId):
    category = Category.objects.get(categoryId=categoryId)
    products = Product.objects.filter(category=category)

    # Serialize the products queryset
    products_list = []
    for product in products:
        products_list.append({
            'productId': product.productId,
            'name': product.name,
            'price': product.price,
            'stock_quantity': product.stock_quantity,
            'created_at': product.created_at.isoformat(),
        })

    return JsonResponse({'products': products_list})

def update_category_info(request, categoryId):
    category = get_object_or_404(Category, categoryId=categoryId)

    if request.method == 'POST':
        print("Hi there")
        edit_category_form = EditCategoryForm(request.POST, request.FILES, instance=category)

        # Check if the form is valid before saving
        if edit_category_form.is_valid():
            print("form is valid")
            edit_category_form.save()  # This saves the updated category

    else:
        edit_category_form = EditCategoryForm(instance=category)
    
    return render(request, 'core/owner/inventory.html')

def delete_category_image(request):
    
    if request.method == "POST":
        categoryId = request.POST.get("id")
        
        # Find the product by productId
        category = get_object_or_404(Category, categoryId=categoryId)
        
        # Check if the product has an associated video
        if category.image:
            category.image.delete()  # Deletes the related ProductVideo object
            category.image = None
            category.save()
            
            # Return a success response
            return JsonResponse({'success': True, 'message': 'Image deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'error': 'No image associated with this product.'})

    # If the request method is not POST, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def update_product_info(request, productId):
    # Retrieve the product instance using the productId
    user = request.user
    product = get_object_or_404(Product, productId=productId)
    product_video = product.video
    print(product_video)

    if request.method == 'POST':
        # Initialize the main product form
        print(request.POST)
        edit_product_form = EditProductForm(request.POST, request.FILES, instance=product)

        # Retrieve all MoreProductVideo instances related to the product
        more_videos = product.more_product_videos.all()
        more_images = product.more_product_images.all()

        if edit_product_form.is_valid():
            print(request.FILES)

            if request.FILES.get('video'):
                # A new video is uploaded
                new_video_file = request.FILES['video']
                
                # Create a new ProductVideo instance
                product_video = ProductVideo.objects.create(
                    created_by=request.user,
                    video=new_video_file,
                    description=request.POST.get('video-description', "")  # Get description from POST
                )
                product.video = product_video

            else:

                if product_video:
                    product_video.description = request.POST.get('video-description', product_video.description)
                    product_video.save()
                    product.video = product_video

            # Save the product form
            edit_product_form.save()

            # Loop through the existing MoreProductVideo instances
            for more_image in more_images:
                image_file_field = f"image-{more_image.mpiId}"

                # Extract the video file and description for this video
                new_image_file = request.FILES.get(image_file_field)

                # Check if there is a new video file or description
                if new_image_file:
                    more_image.image = new_image_file  # Directly assign the new video file
                    more_image.save()  # Save to persist the video update
            
            # Handling more product images
            # Collect all uploaded images
            for index in range(1, len(request.FILES) + 1):
                image_key = f'image-{index}'  # Assuming fields are named as 'image1', 'image2', etc.
                if image_key in request.FILES:
                    image = request.FILES[image_key]
                    more_product_image = MoreProductImage(
                        product=product,
                        image=image
                    )
                    more_product_image.save()

            # Loop through the existing MoreProductVideo instances
            for more_video in more_videos:
                video_file_field = f"video-{more_video.mpvId}"
                description_field = f"video-description-{more_video.mpvId}"

                # Extract the video file and description for this video
                new_video_file = request.FILES.get(video_file_field)
                new_video_description = request.POST.get(description_field)
                print(f"Processing MoreVideo: {more_video.mpvId} with new_video_file: {new_video_file} and new_video_description: {new_video_description}")

                # Check if there is a new video file or description
                if new_video_file or new_video_description:
                    # Update the existing video instance
                    if new_video_file:
                        more_video.video = new_video_file  # Directly assign the new video file
                        more_video.save()  # Save to persist the video update
                        print(f"Updated video for MoreVideo: {more_video.mpvId}")

                    if new_video_description:
                        more_video.description = new_video_description  # Update the description
                        print(f"Updated description for MoreVideo: {more_video.mpvId}")

                    # Save the updated MoreProductVideo instance
                    more_video.save()
                    print(more_video)
                    print(f"MoreVideo {more_video.mpvId} saved.")
            
            # Handling more product videos
            # Collect all uploaded videos and their descriptions
            for index in range(1, len(request.FILES) + 1):
                video_key = f'video-{index}'
                if video_key in request.FILES:
                    video = request.FILES[video_key]
                    description_key = f'video-description-{index}'
                    video_description = request.POST.get(description_key, "")
                    
                    more_product_video = MoreProductVideo(
                        product=product,
                        video=video,
                        description=video_description
                    )
                    more_product_video.save()

        print('Product and videos updated successfully.')

    else:
        edit_product_form = EditProductForm(instance=product)

    # Retrieve existing images and videos for the context
    more_product_images = product.more_product_images.all()

    context = {
        'edit_product_form': edit_product_form,
        'more_product_images': more_product_images,
        'categories': Category.objects.all(),
    }

    context.update(inventory_context(user))

    return render(request, 'core/owner/inventory.html', context)

def get_updated_stock(request):
    if request.method == 'GET':
        # Retrieve all products and their stock quantities
        products = Product.objects.all()
        product_data = []

        for product in products:
            product_data.append({
                'productId': product.productId,  # or product.productId if that's your field name
                'stock_quantity': product.stock_quantity,
            })

        return JsonResponse({'success': True, 'products': product_data})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def delete_product_video(request):
    
    if request.method == "POST":
        productId = request.POST.get("id")
        
        # Find the product by productId
        product = get_object_or_404(Product, productId=productId)
        
        # Check if the product has an associated video
        if product.video:
            product.video.delete()  # Deletes the related ProductVideo object
            product.video = None
            product.save()
            
            # Return a success response
            return JsonResponse({'success': True, 'message': 'Video deleted successfully.'})
        else:
            return JsonResponse({'success': False, 'error': 'No video associated with this product.'})

    # If the request method is not POST, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def delete_transaction_log(request):
    if request.method == "POST":
        transactionLogId = request.POST.get("id")
        
        # Get the transaction log and delete it
        transaction_log = get_object_or_404(TransactionLog, transactionLogId=transactionLogId)
        transaction_log.delete()
        
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request method."})

def delete_more_product_image(request):
    
    if request.method == "POST":
        mpiId = request.POST.get("id")
        print(mpiId)
        
        # Get the MoreProductImage object and delete it
        more_product_image = get_object_or_404(MoreProductImage, mpiId=mpiId)
        print(f"Found MoreProductImage: {more_product_image}")
        
        # Optionally, you can delete the associated image file from storage
        if more_product_image.image and more_product_image.image.name != "more_product_image.jpg":
            more_product_image.image.delete(save=False)  # Deletes the file from the filesystem

        more_product_image.delete()
        
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method."})

def delete_more_product_video(request):
    
    if request.method == "POST":
        mpvId = request.POST.get("id")
        
        # Get the MoreProductImage object and delete it
        more_product_video = get_object_or_404(MoreProductVideo, mpvId=mpvId)
        
        
        # Optionally, you can delete the associated image file from storage
        if more_product_video.video and more_product_video.video.name != "more_product_video.jpg":
            more_product_video.video.delete(save=False)  # Deletes the file from the filesystem

        more_product_video.delete()
        
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method."})

@login_required
def delete_product(request):
    user = request.user

    if request.method == "POST":
        productId = request.POST.get("id")
        # Get the product and delete it
        product = get_object_or_404(Product, productId=productId, created_by=user)
        product.delete()
        
        # Optionally, return the updated product count
        product_count = Product.objects.filter(created_by=user).count()
        
        return JsonResponse({"success": True, "product_count": product_count})

    # Handle GET request
    products = Product.objects.filter(created_by=user).order_by('-created_at')

    return render(request, "core/owner/inventory.html", {
        'products': products,
    })

def add_stock(request):
    if request.method == "POST":
        productId = request.POST.get("id")
        quantity = int(request.POST.get("quantity"))
        print(productId)
        print(quantity)

        try:
            print(quantity)
            product = Product.objects.get(productId=productId)
            product.stock_quantity += quantity  # Increase stock by the provided quantity
            product.save()

            # Log the transaction
            TransactionLog.objects.create(
                product=product,
                action='add',
                quantity=quantity,
            )

            return JsonResponse({
                "success": True, 
                "new_stock": product.stock_quantity  # Send the updated stock back to the client
            })
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found."})
    return JsonResponse({"success": False, "error": "Invalid request."})

def sell_stock(request):
    if request.method == "POST":
        productId = request.POST.get("id")
        quantity = int(request.POST.get("quantity"))

        try:
            product = Product.objects.get(productId=productId)
            product.stock_quantity -= quantity  # Decrease stock by the provided quantity
            product.save()

            # Log the transaction
            TransactionLog.objects.create(
                product=product,
                action='sell',
                quantity=quantity,
            )

            return JsonResponse({
                "success": True, 
                "new_stock": product.stock_quantity  # Send the updated stock back to the client
            })
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product not found."})
    return JsonResponse({"success": False, "error": "Invalid request."})

def undo_last_transaction(request):
    if request.method == "POST":
        productId = request.POST.get("id")  # Get the product ID from the AJAX request

        try:
            # Retrieve the product using the product_id
            product = Product.objects.get(productId=productId)

            # Fetch the last transaction for this product, ordered by timestamp
            last_transaction = TransactionLog.objects.filter(product=product).order_by('-timestamp').first()

            if last_transaction:
                # Undo the last transaction based on the action type
                if last_transaction.action == 'add':
                    product.stock_quantity -= last_transaction.quantity  # Decrease stock if last action was 'add'

                elif last_transaction.action == 'sell':
                    product.stock_quantity += last_transaction.quantity  # Increase stock if last action was 'sell'

                # Save the updated product stock
                product.save()

                # Optionally, delete the last transaction since it's undone
                last_transaction.delete()

                # Return the new stock quantity in the JSON response
                return JsonResponse({
                    "success": True, 
                    "message": "Last transaction undone.", 
                    "new_stock": product.stock_quantity  # Include the updated stock quantity
                })
            else:
                return JsonResponse({"success": False, "message": "No transaction found to undo."})

        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    print("Invalid request method.")  # Debug log
    return JsonResponse({"success": False, "message": "Invalid request method."})

@login_required
def delete_category(request):
    user = request.user

    if request.method == "POST":
        categoryId = request.POST.get("id")
        # Get the product and delete it
        category = get_object_or_404(Category, categoryId=categoryId, created_by=user)
        category.delete()
        
        # Optionally, return the updated product count
        category_count = Category.objects.filter(created_by=user).count()
        
        return JsonResponse({"success": True, "category_count": category_count})

    # Handle GET request
    categories = Category.objects.filter(created_by=user).order_by('-created_at')

    return render(request, "core/owner/inventory.html", {
        'categories': categories,
    })

######################################################################################
####################################### Common #######################################
######################################################################################

@login_required
def account(request):
    user = request.user
    profile = Profile.objects.get(created_by=user)
    notifications = Notification.objects.filter(created_by=user).order_by('-created_at')

    return render(request, "core/owner/account.html", {
        'user': user,
        'profile': profile,
        'notifications': notifications,
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
        'user': user,
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
