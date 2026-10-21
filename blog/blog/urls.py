from django.contrib import admin
from django.urls import path, re_path
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
    path('order/new/', views.create_order, name='create_order'),
    re_path(r'^order/(?P<order_id>\d+)$', views.get_order, name='get_order'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
