from django.urls import path     							
from . import views 

urlpatterns = [									
    path('', views.index),     
    path('home/', views.home, name="home"),     
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),

    path('create_theme/', views.create_theme, name="create_theme"), 
    path('theme/<int:theme_id>/', views.theme, name="theme"), 
    path('delete_theme/<int:theme_id>/', views.delete_theme, name="delete_theme"), 

    path('create_post/', views.create_post, name="create_post"), 
    path('edit_post/<int:post_id>/', views.edit_post, name="edit_post"),
    path('delete_post/<int:post_id>/', views.delete_post, name="delete_post"),

    path('search/', views.search, name="search")
]