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
    path('cake/variant/<int:pk>/',views.CakeVaraintsView.as_view(),name='cake-variants'),
    path('cake/variant/<int:pk1>/<int:pk2>/detail/',views.CakeVariantDetailView.as_view(),name='variant'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
