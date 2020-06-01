"""livestock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('shop.urls', namespace='shop')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('cart/', include('shop.urls')),
    path('pay/', include('shop.urls')),
    path('checkout/', include('shop.urls')),
    path('cart/checkout/', include('shop.urls')),
    path('product/<slug>/', include('shop.urls')),
    path('add_to_cart/<slug>/', include('shop.urls')),
    path('remove_from_cart/<slug>/', include('shop.urls')),
    path('mymarket/', include('shop.urls')),
    path('farmer/', include('shop.urls')),
    path('farmer_register/', include('shop.urls')),
    path('upload/', include('shop.urls'))
    





]

