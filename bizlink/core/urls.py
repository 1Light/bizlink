from django.urls import path

from . import views

app_name = "core"

urlpatterns = [

    # Path for both
    path("owner/home/account/", views.account, name="account"),
    path("owner/account/notification/", views.notification, name="notification"),

    # Path for the owner

    ## Admin
    path("owner/home/admin/", views.admin, name="admin"),
    path("owner/home/admin/update_shop/", views.update_shop, name="update_shop"),
    path("owner/home/admin/create_feature/", views.create_feature, name="create_feature"),
    path('owner/home/admin/add_featured_product/', views.add_featured_product, name='add_featured_product'),
    path('owner/home/admin/delete_featured_product/', views.delete_featured_product, name="delete_featured_product"),
    path('owner/home/admin/add_new_arrival/', views.add_new_arrival, name='add_new_arrival'),
    path('owner/home/admin/delete_new_arrival/', views.delete_new_arrival, name="delete_new_arrival"),
    path('owner/home/admin/delete_feature/', views.delete_feature, name="delete_feature"),

    ## Category
    path("owner/home/categories/", views.category, name="category"),
    path("owner/home/category/<categoryId>/", views.category_detail, name="category_detail"),

    ## Product
    path("owner/home/products/", views.product, name="product"),
    path("owner/home/product/<productId>/", views.product_detail, name="product_detail"),
    path('owner/home/product/apply-discount/<productId>/', views.apply_discount, name='apply_discount'),
    path('owner/home/product/delete-discount/<productId>/', views.delete_discount, name='delete_discount'),
    path("owner/home/products/tag/<slug:tag_slug>/", views.tag, name="tag"),

    ## Factory
    path("owner/factory/", views.factory, name="factory"),
    path("owner/home/inventory/get_updated_stock/", views.get_updated_stock, name="get_updated_stock"),

    ## Inventory
    path("owner/home/inventory/", views.inventory, name="inventory"),
    path("owner/home/inventory/delete_product/", views.delete_product, name="delete_product"),
    path("owner/home/inventory/add_stock/", views.add_stock, name="add_stock"),
    path("owner/home/inventory/sell_stock/", views.sell_stock, name="sell_stock"),
    path("owner/home/inventory/undo_last_transaction/", views.undo_last_transaction, name="undo_last_transaction"),
    path("owner/home/inventory/delete_category/", views.delete_category, name="delete_category"),
    path("owner/home/inventory/delete_transaction_log/", views.delete_transaction_log, name="delete_transaction_log"),
    path("owner/home/inventory/delete_more_product_image/", views.delete_more_product_image, name="delete_more_product_image"),
    path("owner/home/inventory/delete_more_product_video/", views.delete_more_product_video, name="delete_more_product_video"),
    path("owner/home/inventory/delete_product_video/", views.delete_product_video, name="delete_product_video"),
    path("owner/home/inventory/update_product_info/<productId>", views.update_product_info, name="update_product_info"),
    path("owner/home/inventory/category_inventory_view/<categoryId>/", views.category_inventory_view, name="category_inventory_view"),
    path("owner/home/inventory/update_category_info/<categoryId>", views.update_category_info, name="update_category_info"),
    path("owner/home/inventory/delete_category_image/", views.delete_category_image, name="delete_category_image"),

    ## Search
    path("owner/home/search/", views.search, name="search"),
    path("owner/home/search/filter_searched_product/", views.filter_searched_product, name="filter_searched_product"),

    ## Wishlist
    path("owner/wishlist/", views.wishlist, name="wishlist"),

    ## Shop
    path("owner/shop/", views.owner_shop, name="owner_shop"),
    path("owner/shop/add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),

    # Path for the Customer Pages
    
    path("customer/home/", views.customer_home, name="customer_home"),
    path("customer/shops/", views.shop, name="shop"),
    path("customer/shops/visit_shop/<shopId>/", views.visit_shop, name="visit_shop"),
]