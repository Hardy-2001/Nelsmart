from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop/', views.shop, name='shop'),
    path('checkout/', views.checkout, name='checkout'),
    path('free-site-visit/', views.free_site_visit, name='free_site_visit'),
    path('get-informed/', views.get_informed, name='get_informed'),
    path('info/street-light/', views.street_light, name='street_light'),
    path('info/lithium-battery/', views.lithium_battery, name='lithium_battery'),
    path('info/solar-system/', views.solar_system, name='solar_system'),
    path('info/solar-farm/', views.solar_farm, name='solar_farm'),

    path('info/<str:slug>/', views.info_detail, name='info_detail'),
    path('like/<str:slug>/', views.like_article, name='like_article'),
    path('solar-cost/', views.solar_cost, name='solar_cost'),
    path('solar-only-cost/', views.solar_only_cost, name='solar_only_cost'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:id>/', views.project_detail, name='project_detail'),
    path('return-policy/', views.return_policy, name='return_policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('payment-delivery/', views.payment_delivery, name='payment_delivery'),
    path('terms/', views.terms, name='terms'),
    path('about/', views.about, name='about'),
    path('culture', views.culture, name='culture'),
    path('basic-plan', views.basic_plan, name='basic_plan'),
    path('standard-plan/', views.standard_plan, name='standard_plan'),
    path('premium-plan/', views.premium_plan, name='premium_plan'),
]
