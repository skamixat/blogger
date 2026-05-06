from django.contrib import admin
from django.urls import path
from main_blog.views import *

urlpatterns = [
   path('', BlogHome.as_view(), name='home'),
   path('categories/', categories),
   path('about/', about, name='about'),
   path('add_page/', AddPage.as_view(), name='add_page'),
   path('login/', LoginUser.as_view(), name='login'),
   path('rigister/', RegisterUser.as_view(), name='register'),
   path('logout/', logout_user, name='logout'),
   path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
   path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'),
]