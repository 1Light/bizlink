from django.db import models
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from django.db.models import Sum

# Creating Status Choices for Products
STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
)

# Creating Rating for Products and Shops
RATING = (
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
)

# Creating Status for Products
STATUS = (
        ('draft', 'Draft'),
        ('disabled', 'Disabled'),
        ('rejected', 'Rejected'),
        ('in_review', 'In Review'),
        ('published', 'Published'),
)

# Custom file upload path for shop images
def shop_directory_path(instance, filename):
    return 'user_{0}/shop_{1}/{2}'.format(instance.created_by.id, instance.shopId, filename)

# Custom file upload path for category images
def category_directory_path(instance, filename):
    return 'user_{0}/shop_{1}/category_{2}/{3}'.format(
        instance.created_by.id, instance.shop.shopId, instance.categoryId, filename
    )

# Custom file upload path for product images
def product_directory_path(instance, filename):
    return 'user_{0}/shop_{1}/category_{2}/product_{3}/{4}'.format(
        instance.created_by.id, instance.shop.shopId, instance.category.categoryId, instance.productId, filename
    )

# Custom file upload path for product videos
def product_video_directory_path(instance, filename):
    return 'user_{0}/shop_{1}/category_{2}/product_{3}/videos/{4}'.format(
        instance.created_by.id, instance.shop.shopId, instance.category.categoryId, instance.productId, filename
    )


# Custom file upload path for more product images
def mpi_directory_path(instance, filename):
    return 'user_{0}/shop_{1}/category_{2}/product_{3}/more_images/{4}'.format(
        instance.product.created_by.id, instance.product.shop.shopId, instance.product.category.categoryId, instance.product.productId, filename
    )

# Custom file upload path for more product videos
def mpv_directory_path(instance, filename):
    return 'user_{0}/shop_{1}/category_{2}/product_{3}/more_videos/{4}'.format(
        instance.product.created_by.id, instance.product.shop.shopId, instance.product.category.categoryId, instance.product.productId, filename
    )

# Custom file upload path for feature images
def feature_directory_path(instance, filename):
    return 'user_{0}/shop_{1}/feature_{2}/{3}'.format(
        instance.shop.created_by.id, instance.shop.shopId, instance.featureId, filename
    )

# Create your models here.
class Tag(models.Model):
    pass

class ProductVideo(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_videos', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='product_video_directory_path', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Videos"
    
    def __str__(self):
        return str(self.video)

class Shop(models.Model):
    shopId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="shop", alphabet="ABCDEF0123456789")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='shop_directory_path', blank=True, null=True)

    address = models.TextField(blank=False, null=False)
    contact = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_shop")

    class Meta:
        ordering = ('name',)
        unique_together = ('created_by', 'name')
    
    def __str__(self):
        return self.name
    
    def shop_image(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
        else:
            # Return a placeholder or default image
            return "No Image Available"

class Category(models.Model):
    categoryId =  ShortUUIDField(unique=True, length=10, max_length=21, prefix="category", alphabet="ABCDEF0123456789")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='category_directory_path', blank=True, null=True)
    shop = models.ForeignKey(Shop, related_name='shop_categories', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_categories")

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        unique_together = ('created_by', 'name')
    
    def __str__(self):
        return self.name
    
    def category_image(self):
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
        return ""
    
    def total_value(self):
        return self.category_products.aggregate(total=Sum('price'))['total'] or 0.00

class Product(models.Model):
    productId =  ShortUUIDField(unique=True, length=10, max_length=21, prefix="product", alphabet="ABCDEF0123456789")

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='category_products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_directory_path', blank=True, null=True)
    video = models.ForeignKey(ProductVideo, null=True, blank=True, on_delete=models.SET_NULL, related_name="product_on_the_video")

    shop = models.ForeignKey(Shop, related_name='shop_products', on_delete=models.CASCADE)

    description = models.TextField(blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    
    mfg = models.DateTimeField(auto_now_add=False, null=True, blank=True)  

    price = models.DecimalField(max_digits=15, decimal_places=2)

    stock_quantity = models.PositiveIntegerField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="0123456789")

    class Meta:
        ordering = ('name',)
        unique_together = ('created_by', 'name', 'category')
    
    def __str__(self):
        return self.name
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
    
    def check_stock_status(self):
        if self.stock_quantity > 0:
            return "In Stock"
        else:
            return "Out of Stock"
    
    def get_mfg_display(self):
        if self.mfg:
            return self.mfg
        return "Not Specified"
    
class DiscountedProduct(models.Model):
    discountProductId = ShortUUIDField(unique=True, length=10, max_length=27, prefix="discountedProduct", alphabet="ABCDEF0123456789")

    shop = models.ForeignKey(Shop, related_name='shop_discounted_products', on_delete=models.CASCADE)

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discounted_product')
    new_price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_until = models.DateTimeField(null=True, blank=True) 
    has_discount_ended = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_discounted_products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('product__name',)
        verbose_name_plural = "Discounted Products"
        unique_together = ('shop', 'product')
    
    def __str__(self):
        return self.product.name
    
    def discounted_product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.product.image.url))
    
    def product_name(self):
        return self.product.name

    def product_price(self):
        return self.product.price
    
    def get_percentage(self):
        if self.new_price > 0:
            discount = 100 - ((self.new_price / self.product.price) * 100)
            return discount
        return 0

class MoreProductImage(models.Model):
    mpiId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="mpi", alphabet="ABCDEF0123456789")

    image = models.ImageField(upload_to='mpi_directory_path', blank=True, null=True)
    product = models.ForeignKey(Product, related_name='more_product_images', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "More Product Images"
    
    def __str__(self):
        return str(self.image)
    
    def more_product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))

class MoreProductVideo(models.Model):
    mpvId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="mpv", alphabet="ABCDEF0123456789")

    video = models.FileField(upload_to='mpv_directory_path', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    product = models.ForeignKey(Product, related_name='more_product_videos', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "More Product Videos"
    
    def __str__(self):
        return str(self.video)
    
    def more_product_video(self):
        if self.video:
            return mark_safe(f'<video width="100" height="100" controls><source src="{self.video.url}" type="video/mp4"></video>')
        return "No video available"

class TransactionLog(models.Model):
        
    ACTION_CHOICES = [
        ('add', 'Add'),
        ('sell', 'Sell'),
    ]
    
    transactionLogId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="tlog", alphabet="ABCDEF0123456789")
    product = models.ForeignKey(Product, related_name='product_transaction_logs', on_delete=models.CASCADE)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)  # 'add' or 'sell'
    quantity = models.PositiveIntegerField()  
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction Log"
        verbose_name_plural = "Transaction Logs"

    def __str__(self):
        return f"{self.product.name} - {self.action} - {self.quantity}"
    
    def product_name(self):
        return self.product.name

    
######################### Cart, Order, OrderItems, and Address ######################### 
######################### Cart, Order, OrderItems, and Address ######################### 
######################### Cart, Order, OrderItems, and Address #########################  

class CartOrder(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_cart_orders', on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=15, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)

    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='processing')

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderProduct(models.Model):
    order = models.ForeignKey(CartOrder, related_name='cart_order_products', on_delete=models.CASCADE)

    invoice_number = models.CharField(max_length=255)

    product_status = models.CharField(max_length=255)
    product = models.CharField(max_length=255)

    image = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)

    price = models.DecimalField(max_digits=15, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=15, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Products"

    def cart_order_product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
    
######################### Product Review, Wishlist ######################### 
######################### Product Review, Wishlist ######################### 
######################### Product Review, Wishlist #########################

class ProductReview(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_product_reviews', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='product_reviews', on_delete=models.CASCADE)

    review = models.TextField()
    rating = models.PositiveIntegerField(choices=RATING, default=None)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
    
    def __str__(self):
        return self.product.name
    
    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_wishlists', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist_product', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"
    
    def __str__(self):
        return self.product.name

################################## Features, Featured Products ##################################
################################## Features, Featured Products ##################################
################################## Features, Featured Products ##################################

class Feature(models.Model):
    featureId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="feature", alphabet="ABCDEF0123456789")

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='feature_directory_path', blank=True, null=True)
    shop = models.ForeignKey(Shop, related_name='shop_features', on_delete=models.CASCADE)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_features', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        unique_together = ('created_by', 'name')
    
    def __str__(self):
        return self.name
    
    def feature_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))

class FeaturedProduct(models.Model):
    featuredProductId = ShortUUIDField(unique=True, length=10, max_length=27, prefix="featuredProduct", alphabet="ABCDEF0123456789")

    shop = models.ForeignKey(Shop, related_name='shop_featured_products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_featured_products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, related_name='product_featured_product', on_delete=models.CASCADE)

    class Meta:
        ordering = ('product__name',)
        unique_together = ('shop', 'product')
        verbose_name_plural = 'Featured Products'
    
    def __str__(self):
        return self.product.name
    
    def featured_product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.product.image.url))
    
class NewArrival(models.Model):
    newArrivalId = ShortUUIDField(unique=True, length=10, max_length=23, prefix="newArrival", alphabet="ABCDEF0123456789")

    shop = models.ForeignKey(Shop, related_name='shop_new_arrival', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_new_arrival', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    product = models.ForeignKey(Product, related_name='product_new_arrival', on_delete=models.CASCADE)

    class Meta:
        ordering = ('product__name',)
        unique_together = ('shop', 'product')
        verbose_name_plural = 'New Arrivals'
    
    def __str__(self):
         return self.product.name
    
    def new_arrival_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.product.image.url))
