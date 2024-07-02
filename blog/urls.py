from django.urls import path
from . import views

app_name = 'blog'  # Ensure this is set

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('', views.blog_home, name='blog_home'),
]
