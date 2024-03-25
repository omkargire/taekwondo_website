from django.urls import path, include
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home",views.home, name="home"),
    path("signup",views.signup, name="signup"),
    path("signin",views.signin, name="signin"),
    path("admission", views.admission, name="admission"),
    path("contact", views.contact, name="contact"),
    path("store", views.store, name="store"),
    path("Demo",views.Demo, name="Demo"),
    path("store/product/<int:product_id>/", views.product, name="product"),
    path("store/product/purchase/<int:product_id>/", views.purchase, name="purchase"),
    path("confirm_purchase/<int:product_id>/", views.confirm_purchase, name="confirm_purchase"),
    path("trainers", views.trainers_page, name="trainers"),
]
