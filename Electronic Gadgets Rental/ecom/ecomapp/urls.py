from django.contrib import admin
from django.urls import path
from ecomapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('usrlogin', views.usrlogin, name="usrlogin"),
    path('logout', views.logout, name="logout"),
    path('usr_details', views.usr_details, name="usr_details"),
    path('home', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('gamingsec', views.gamingsec, name="gamingsec"),
    path('domesticsec', views.domesticsec, name="domesticsec"),
    path('systemadmin', views.systemadmin, name="systemadmin"),
    path('admin_odr', views.admin_odr, name="admin_odr"),
    path('cart/<int:id>', views.cart, name="cart"),
    path('view_cart', views.view_cart, name="view_cart"),
    path('application', views.application, name="application"),
    path('application2', views.application2, name="application2"),
    path('del_application/<int:id>', views.del_application, name="del_application"),
    path('adm_del_application/<int:id>', views.adm_del_application, name="adm_del_application"),
    path('adm_approve/<int:id>', views.adm_approve, name="adm_approve"),
    path('buyproduct/<int:id>', views.buyproduct, name="buyproduct"),
    path('renteditems', views.renteditems, name="renteditems"),
    path('validate_customer', views.validate_customer, name="validate_customer"),
]