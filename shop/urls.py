from django.urls import path
from . import views
from livestock import settings
from django.conf.urls.static import static


app_name= "shop"

urlpatterns=[
	path('', views.index, name='home'),
	path('cart/', views.OrderSummaryView.as_view(), name='cart'),
	
	path('pay/', views.pay, name='pay'),
	path('error1/', views.error1, name='error1'),
	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('report_view/', views.report_view, name='report_view'),
	path('withdraw_request/', views.withdraw_request, name='withdraw_request'),
	path('cart/checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('farmer/', views.post_product, name='post_product'),
	path('cow_search/', views.cow_search, name='cow_search'),
	path('payment/<payment_option>/', views.PaymentView.as_view(), name='payment'),
	path('farmer_register/', views.reg_farmer, name='reg_farmer'),
	path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
	path('order-summary2/', views.OrderSummaryView_farmer.as_view(), name='order-summary2_'),
	path('product/<slug>/', views.product, name='product'),
	path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
	path('farm_market/<slug>/', views.farmDetailView.as_view(), name='farmDetailView'),
	path('farm_market', views.farmDetailView.as_view(), name='farmDetailView'),
	path('cowView/', views.cowView.as_view(), name='cowView'),
	path('goatView/', views.goatView.as_view(), name='goatView'),
	path('rabbitsView/', views.rabbitsView.as_view(), name='rabbitsView'),
	path('ducksView/', views.ducksView.as_view(), name='ducksView'),
	path('sheepView/', views.sheepView.as_view(), name='sheepView'),
	path('chickenView/', views.chickenView.as_view(), name='chickenView'),
	path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
	path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
	path('mymarket/', views.MarketView.as_view(), name='mymarket'),
	path('product_upload/', views.product_upload, name='product_upload')




]
#path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),path('register/', views.MyRegistrationView.as_view(), name='registration_register'),

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)