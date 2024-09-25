from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.contrib import messages
from django.db.models import Q
from taggit.models import Tag
from django.template.loader import render_to_string

from shop.forms import EditShop, CreateFeature

from shop.models import Shop, Category, Product, MoreProductImage, CartOrder, CartOrderProduct, ProductReview, Wishlist, Address, Feature, FeaturedProduct, NewArrival

############################ Views for Business Owners ############################
############################ Views for Business Owners ############################
############################ Views for Business Owners ############################

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
    products = Product.objects.filter(created_by=user).order_by("-created_at")

    return render(request, "core/owner/product.html", {
        'products': products,
    })

def product_detail(request, productId):
    user = request.user
    product = Product.objects.get(created_by=user, productId=productId)
    product_images = product.more_product_images.all()
    product_videos = product.more_product_videos.all()
    print(product_videos.exists())
    shop = Shop.objects.get(created_by=user)
    related_products = Product.objects.filter(category=product.category).exclude(productId=productId)

    return render(request, "core/owner/product-detail.html", {
        'product': product,
        'product_images': product_images,
        'product_videos': product_videos,
        'shop': shop,
        'related_products':  related_products,
    })

def category(request):
    user = request.user
    categories = Category.objects.filter(created_by=user).order_by("-created_at")

    return render(request, "core/owner/category.html", {
        'categories': categories,
    })

def category_detail(request, categoryId):
    user = request.user
    category = Category.objects.get(created_by=user, categoryId=categoryId)
    products = Product.objects.filter(created_by=user, category=category)

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
def owner_account(request):
    user = request.user

    return render(request, "core/owner/owner-account.html", {
        'user': user,
    })

def add_to_wishlist(request):
    product_id = request.GET.get('id')
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

    return JsonResponse(context)

@login_required
def wishlist(request):
    user = request.user
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

    return render(request, "core/owner/admin.html", {
        'shop': shop,
        'features': features,
        'products': products,
        'create_feature_form': create_feature_form,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
    })

############################ Views for Shops ############################

def update_shop(request):
    user = request.user
    shop = Shop.objects.get(created_by=user)  

    if request.method == 'POST':
        form = EditShop(request.POST, request.FILES, instance=shop)

        if form.is_valid():
            form.save()

            return redirect("core:home") 

    else:
        form = EditShop(instance=shop)

    return render(request, 'core/home.html', {
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
    
    return render(request, "core/home.html", {
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

def customer_home(request):

    return render(request, "core/customer/home.html")

def shop(request):

    shops = Shop.objects.all().order_by("name")

    return render(request, "core/customer/shop.html", {
        'shops': shops
    }) 