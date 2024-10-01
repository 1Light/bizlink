from django.urls import path

from . import views

app_name = "core"

urlpatterns = [

    # Path for the Owner Pages
    path("owner/home/", views.owner_home, name="owner_home"),
    path("owner/home/products/", views.product, name="product"),
    path("owner/home/product/<productId>/", views.product_detail, name="product_detail"),
    path('owner/home/product/apply-discount/<productId>/', views.apply_discount, name='apply_discount'),
    path('owner/home/product/delete-discount/<productId>/', views.delete_discount, name='delete_discount'),
    path("owner/home/categories/", views.category, name="category"),
    path("owner/home/category/<categoryId>/", views.category_detail, name="category_detail"),
    path("owner/home/products/tag/<slug:tag_slug>/", views.tag, name="tag"),
    path("owner/home/admin/", views.admin, name="admin"),
    path("owner/home/search/", views.search, name="search"),
    path("owner/home/search/filter_searched_product/", views.filter_searched_product, name="filter_searched_product"),
    path("owner/home/account/", views.owner_account, name="owner_account"),
    path("owner/wishlist/", views.wishlist, name="wishlist"),
    path("owner/account/notification/", views.notification, name="notification"),

    # Path for Shops

    ## Admin
    path("owner/home/admin/update_shop/", views.update_shop, name="update_shop"),
    path("owner/home/admin/create_feature/", views.create_feature, name="create_feature"),
    path('owner/home/admin/add_featured_product/', views.add_featured_product, name='add_featured_product'),
    path('owner/home/admin/delete_featured_product/', views.delete_featured_product, name="delete_featured_product"),
    path('owner/home/admin/add_new_arrival/', views.add_new_arrival, name='add_new_arrival'),
    path('owner/home/admin/delete_new_arrival/', views.delete_new_arrival, name="delete_new_arrival"),
    path("owner/home/add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),

    ## Shop
    path("owner/shop/", views.owner_shop, name="owner_shop"),

    # Path for the Customer Pages
    path("customer/home/", views.customer_home, name="customer_home"),
    path("customer/shops/", views.shop, name="shop"),
    path("customer/shops/visit_shop/<shopId>/", views.visit_shop, name="visit_shop"),
]