from django.db import models
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field

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

class Address(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_addresses', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

class ProductVideo(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_videos', on_delete=models.CASCADE)
    description = CKEditor5Field('Description' ,blank=True, null=True, default="This is a demo video for the product", config_name='extends')
    video = models.FileField(upload_to='product_video_directory_path', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Videos"
    
    def __str__(self):
        return str(self.video)

class Shop(models.Model):
    shopId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="shop", alphabet="ABCDEF0123456789")

    name = models.CharField(max_length=255, default="Nestify")
    description = CKEditor5Field('Description', blank=False, null=False, default="This is a shop", config_name='extends')
    image = models.ImageField(upload_to='shop_directory_path', blank=True, null=True)

    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    contact = models.CharField(max_length=255, default="+251 97 654 2331")

    chat_resp_time = models.CharField(max_length=255, default="100")
    shipping_on_time = models.CharField(max_length=255, default="100")
    authentic_rating = models.CharField(max_length=255, default="100")
    days_return = models.CharField(max_length=255, default="100")
    warranty_period = models.CharField(max_length=255, default="100")

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

    name = models.CharField(max_length=255, default="Food")
    description = CKEditor5Field('Description', blank=False, null=False, default="This is a category", config_name='extends')
    image = models.ImageField(upload_to='category_directory_path', blank=True, null=True, default="category.jpg")
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
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))

class Product(models.Model):
    productId =  ShortUUIDField(unique=True, length=10, max_length=21, prefix="product", alphabet="ABCDEF0123456789")

    name = models.CharField(max_length=255, default="Fresh Pear")
    category = models.ForeignKey(Category, related_name='category_products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_directory_path', blank=True, null=True, default="product.jpg")
    video = models.ForeignKey(ProductVideo, null=True, blank=True, on_delete=models.SET_NULL, related_name="product_on_video")

    shop = models.ForeignKey(Shop, related_name='shop_products', on_delete=models.CASCADE)

    description = CKEditor5Field('Description', blank=True, null=True, default="This is the product", config_name='extends')
    specifications = CKEditor5Field('Specifications', blank=True, null=True, config_name='extends')
    
    life = models.CharField(max_length=255, default="Not Specified", null=True, blank=True)
    mfg = models.DateTimeField(auto_now_add=False, null=True, blank=True)  

    price = models.DecimalField(max_digits=15, decimal_places=2, default=1.99)
    old_price = models.DecimalField(max_digits=15, decimal_places=2, default=2.99)

    stock_quantity = models.PositiveIntegerField(default="5")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)
    product_status = models.CharField(max_length=20, choices=STATUS, default='in_review')
    status = models.BooleanField(default=True)

    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="0123456789")

    class Meta:
        ordering = ('name',)
        unique_together = ('created_by', 'name', 'category')
    
    def __str__(self):
        return self.name
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
    
    def get_percentage(self):
        if self.old_price > 0:
            new_price = (self.price / self.old_price) * 100
            return new_price
        return 0
    
    def check_stock_status(self):
        if self.stock_quantity > 0:
            return "In Stock"
        else:
            return "Out of Stock"

class MoreProductImage(models.Model):
    mpiId = ShortUUIDField(unique=True, length=10, max_length=21, prefix="mpi", alphabet="ABCDEF0123456789")

    image = models.ImageField(upload_to='mpi_directory_path', blank=True, null=True, default="more_product_image.jpg")
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

    video = models.FileField(upload_to='mpv_directory_path', blank=True, null=True, default="more_product_video.jpg")
    description = CKEditor5Field('Description', blank=True, null=True, default="This is a demo video for the product", config_name='extends')

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
    
######################### Product Review, Wishlist and Address ######################### 
######################### Product Review, Wishlist and Address ######################### 
######################### Product Review, Wishlist and Address #########################

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
