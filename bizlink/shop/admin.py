from django.contrib import admin
from .models import Shop, Category, Product, DiscountedProduct, MoreProductImage, CartOrder, CartOrderProduct, ProductReview, Wishlist, Feature, FeaturedProduct, NewArrival, MoreProductVideo, ProductVideo

# Configure Your Admin Models Here
class MoreProductImageAdmin(admin.TabularInline):
    model = MoreProductImage

class MoreProductVideoAdmin(admin.TabularInline):
    model = MoreProductVideo
    extra = 1  # Number of extra empty forms to display for adding new videos (by default it is 3)
    fields = ['mpvId', 'video', 'description']
    readonly_fields = ['mpvId']

class ProductAdmin(admin.ModelAdmin):
    inlines = [MoreProductImageAdmin, MoreProductVideoAdmin]
    list_display = ['created_by', 'name', 'product_image', 'price', 'featured', 'product_status']

class DiscountedProductAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'discounted_product_image', 'product_name', 'product_price', 'new_price', 'discount_until', 'has_discount_ended']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'name', 'category_image']

class ShopAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'name', 'shop_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'product', 'image', 'quantity', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'product', 'review', 'rating', 'created_at']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'product', 'created_at']

class FeatureAdmin(admin.ModelAdmin):
    list_display = ['created_by']

class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'featured_product_image']

class NewArrivalAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'new_arrival_image']

class ProductVideoAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'video', 'description']

# Register Your Models Here
admin.site.register(Product, ProductAdmin)
admin.site.register(DiscountedProduct, DiscountedProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProduct, CartOrderProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(FeaturedProduct, FeaturedProductAdmin)
admin.site.register(NewArrival, NewArrivalAdmin)
admin.site.register(ProductVideo, ProductVideoAdmin)