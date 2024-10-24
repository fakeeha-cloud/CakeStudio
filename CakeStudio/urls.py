"""
URL configuration for CakeStudio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name='register'),
    path('',views.SignInView.as_view(),name='sign-in'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('cakes/<int:pk>/list/',views.CakeListView.as_view(),name='cake-list'),
    path('cake/<int:pk>/variants/',views.CakeVaraintsView.as_view(),name='cake-variants'),
    path('cake/<int:pk1>/variant/<int:pk2>/detail/',views.CakeVariantDetailView.as_view(),name='variant'),
    path('cake/<int:pk>/wishlist/add',views.AddToWishListView.as_view(),name='add-wishlist'),
    path('wishlist/summary/',views.MyWishlistView.as_view(),name='mywishlist'),
    path('wishlist/item/<int:pk>/remove/',views.WishlistItemDeleteView.as_view(),name='wishlist-remove'),
    path('cake/<int:pk>/cart/add',views.AddToCartView.as_view(),name='add-cartItem'),
    path('cart/summary/',views.MyCartView.as_view(),name='mycart'),
    path('cart/item/<int:pk>/update',views.QuantityUpdateView.as_view(),name='cart-update'),
    path('cart/item/<int:pk>/remove',views.CartItemDeleteView.as_view(),name='cartItem-remove'),
   
    path('payment/',views.PaymentView.as_view(),name='payment'),
    path('order/placed/',views.OrderPlacedView.as_view(),name='order-placed'),
    path('payment/verification/',views.PaymentVerificationView.as_view(),name='payment-verify'),
    path('order/summary/',views.MyOrderSummaryView.as_view(),name='order-summary'),
    path('cake/<int:pk>/review-add/',views.ReviewView.as_view(),name='review-add'),
    path('about-us/',views.AboutUsView.as_view(),name='about-us'),
    path('contact-us/',views.ContactUsView.as_view(),name='contact-us'),
    path('signout/',views.SignOutView.as_view(),name='sign-out'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('verify/otp/',views.verifyOtpView.as_view(),name='verify_otp'),
    
   


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
